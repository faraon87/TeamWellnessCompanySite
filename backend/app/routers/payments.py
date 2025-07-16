from fastapi import APIRouter, HTTPException, Depends, Request
from typing import Dict, Any
from datetime import datetime
from emergentintegrations.payments.stripe.checkout import StripeCheckout, CheckoutSessionResponse, CheckoutStatusResponse, CheckoutSessionRequest
from ..models import User, PaymentRequest, PaymentTransaction, WELLNESS_PACKAGES
from ..database import payment_transactions_collection, users_collection
from ..auth import get_current_user, get_optional_user
from ..behavior_tracker import BehaviorTracker
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/api/payments", tags=["payments"])

# Initialize Stripe
STRIPE_API_KEY = os.getenv("STRIPE_API_KEY")

@router.post("/v1/checkout/session")
async def create_checkout_session(
    request: Request,
    payment_request: PaymentRequest,
    current_user: User = Depends(get_optional_user)
):
    """Create Stripe checkout session"""
    try:
        # Validate package
        if payment_request.package_id not in WELLNESS_PACKAGES:
            raise HTTPException(status_code=400, detail="Invalid package ID")
        
        package = WELLNESS_PACKAGES[payment_request.package_id]
        
        # Initialize Stripe checkout
        host_url = str(request.base_url)
        webhook_url = f"{host_url}api/payments/webhook/stripe"
        stripe_checkout = StripeCheckout(api_key=STRIPE_API_KEY, webhook_url=webhook_url)
        
        # Create checkout session
        checkout_request = CheckoutSessionRequest(
            amount=package.price,
            currency="usd",
            success_url=payment_request.success_url,
            cancel_url=payment_request.cancel_url,
            metadata={
                "package_id": payment_request.package_id,
                "package_name": package.name,
                "user_id": current_user.id if current_user else None,
                "user_email": current_user.email if current_user else None,
                **payment_request.metadata
            }
        )
        
        session: CheckoutSessionResponse = await stripe_checkout.create_checkout_session(checkout_request)
        
        # Create payment transaction record
        transaction = PaymentTransaction(
            user_id=current_user.id if current_user else None,
            session_id=session.session_id,
            amount=package.price,
            currency="usd",
            status="initiated",
            payment_status="pending",
            metadata={
                "package_id": payment_request.package_id,
                "package_name": package.name,
                "user_id": current_user.id if current_user else None,
                "user_email": current_user.email if current_user else None,
                **payment_request.metadata
            }
        )
        
        await payment_transactions_collection.insert_one(transaction.dict(exclude={"id"}))
        
        # Track payment initiation
        if current_user:
            await BehaviorTracker.track_action(
                user_id=current_user.id,
                action="initiate_payment",
                page="payments",
                details={
                    "package_id": payment_request.package_id,
                    "amount": package.price,
                    "session_id": session.session_id
                }
            )
        
        return {
            "url": session.url,
            "session_id": session.session_id,
            "package": {
                "id": package.id,
                "name": package.name,
                "price": package.price,
                "features": package.features
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create checkout session: {str(e)}")

@router.get("/v1/checkout/status/{session_id}")
async def get_checkout_status(
    session_id: str,
    current_user: User = Depends(get_optional_user)
):
    """Get checkout session status"""
    try:
        # Initialize Stripe checkout
        stripe_checkout = StripeCheckout(api_key=STRIPE_API_KEY, webhook_url="")
        
        # Get checkout status
        checkout_status: CheckoutStatusResponse = await stripe_checkout.get_checkout_status(session_id)
        
        # Update transaction record
        update_data = {
            "status": checkout_status.status,
            "payment_status": checkout_status.payment_status,
            "updated_at": datetime.utcnow()
        }
        
        await payment_transactions_collection.update_one(
            {"session_id": session_id},
            {"$set": update_data}
        )
        
        # If payment is successful, update user plan
        if checkout_status.payment_status == "paid":
            await _handle_successful_payment(session_id, checkout_status)
        
        return {
            "status": checkout_status.status,
            "payment_status": checkout_status.payment_status,
            "amount_total": checkout_status.amount_total,
            "currency": checkout_status.currency,
            "metadata": checkout_status.metadata
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get checkout status: {str(e)}")

@router.post("/webhook/stripe")
async def stripe_webhook(request: Request):
    """Handle Stripe webhook events"""
    try:
        # Get request body and signature
        webhook_request_body = await request.body()
        stripe_signature = request.headers.get("Stripe-Signature")
        
        # Initialize Stripe checkout
        stripe_checkout = StripeCheckout(api_key=STRIPE_API_KEY, webhook_url="")
        
        # Handle webhook
        webhook_response = await stripe_checkout.handle_webhook(
            webhook_request_body, 
            stripe_signature
        )
        
        # Update transaction record
        if webhook_response.session_id:
            await payment_transactions_collection.update_one(
                {"session_id": webhook_response.session_id},
                {
                    "$set": {
                        "status": webhook_response.event_type,
                        "payment_status": webhook_response.payment_status,
                        "updated_at": datetime.utcnow()
                    }
                }
            )
            
            # Handle successful payment
            if webhook_response.payment_status == "paid":
                await _handle_successful_payment_webhook(webhook_response)
        
        return {"message": "Webhook processed successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Webhook processing failed: {str(e)}")

async def _handle_successful_payment(session_id: str, checkout_status: CheckoutStatusResponse):
    """Handle successful payment - update user plan"""
    try:
        # Get transaction details
        transaction = await payment_transactions_collection.find_one({"session_id": session_id})
        if not transaction:
            return
        
        # Get package info from metadata
        package_id = transaction.get("metadata", {}).get("package_id")
        user_id = transaction.get("user_id")
        
        if user_id and package_id:
            # Update user plan
            await users_collection.update_one(
                {"_id": user_id},
                {
                    "$set": {
                        "plan": package_id,
                        "updated_at": datetime.utcnow()
                    }
                }
            )
            
            # Track successful payment
            await BehaviorTracker.track_action(
                user_id=user_id,
                action="payment_success",
                page="payments",
                details={
                    "package_id": package_id,
                    "amount": checkout_status.amount_total / 100,  # Convert from cents
                    "session_id": session_id
                }
            )
            
            # Award bonus points for upgrade
            await BehaviorTracker.track_action(
                user_id=user_id,
                action="plan_upgrade",
                page="payments",
                details={
                    "new_plan": package_id,
                    "bonus_points": 100
                }
            )
        
    except Exception as e:
        print(f"Error handling successful payment: {e}")

async def _handle_successful_payment_webhook(webhook_response):
    """Handle successful payment from webhook"""
    try:
        # Get transaction details
        transaction = await payment_transactions_collection.find_one({"session_id": webhook_response.session_id})
        if not transaction:
            return
        
        # Get package info from metadata
        package_id = webhook_response.metadata.get("package_id")
        user_id = transaction.get("user_id")
        
        if user_id and package_id:
            # Update user plan
            await users_collection.update_one(
                {"_id": user_id},
                {
                    "$set": {
                        "plan": package_id,
                        "updated_at": datetime.utcnow()
                    }
                }
            )
            
            # Track successful payment
            await BehaviorTracker.track_action(
                user_id=user_id,
                action="payment_success",
                page="payments",
                details={
                    "package_id": package_id,
                    "session_id": webhook_response.session_id,
                    "event_type": webhook_response.event_type
                }
            )
        
    except Exception as e:
        print(f"Error handling webhook payment: {e}")

@router.get("/packages")
async def get_wellness_packages():
    """Get available wellness packages"""
    return {
        "packages": [package.dict() for package in WELLNESS_PACKAGES.values()]
    }

@router.get("/history")
async def get_payment_history(current_user: User = Depends(get_current_user)):
    """Get user's payment history"""
    try:
        transactions_query = payment_transactions_collection.find(
            {"user_id": current_user.id}
        ).sort("created_at", -1).limit(50)
        transactions = await transactions_query.to_list(length=50)
        
        return {"transactions": transactions}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get payment history: {str(e)}")