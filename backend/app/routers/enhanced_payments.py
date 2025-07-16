from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import BaseModel
from typing import Optional, Dict, Any
import os
import uuid
from datetime import datetime
from emergentintegrations.payments.stripe.checkout import (
    StripeCheckout, 
    CheckoutSessionResponse, 
    CheckoutStatusResponse, 
    CheckoutSessionRequest
)
from ..database import get_database, payment_transactions_collection, users_collection
import json

router = APIRouter()

# Initialize Stripe with environment variable
STRIPE_API_KEY = os.getenv('STRIPE_API_KEY')
if not STRIPE_API_KEY:
    print("⚠️  STRIPE_API_KEY not found in environment variables")
    STRIPE_API_KEY = "sk_test_demo_key"  # Fallback for demo

# Payment Models
class PaymentRequest(BaseModel):
    package_id: str
    origin_url: str
    user_id: Optional[str] = None

class CustomPaymentRequest(BaseModel):
    amount: float
    currency: str = "usd"
    origin_url: str
    user_id: Optional[str] = None
    metadata: Optional[Dict[str, str]] = None

class PaymentResponse(BaseModel):
    checkout_url: str
    session_id: str
    payment_id: str

# Fixed wellness packages (security best practice)
WELLNESS_PACKAGES = {
    "basic": {
        "name": "Basic Wellness Plan",
        "amount": 9.99,
        "currency": "usd",
        "description": "Essential wellness programs and basic AI coaching",
        "features": ["Basic programs", "AI wellness tips", "Progress tracking"]
    },
    "plus": {
        "name": "Plus Wellness Plan", 
        "amount": 19.99,
        "currency": "usd",
        "description": "Enhanced wellness programs with advanced AI coaching",
        "features": ["All basic features", "Advanced programs", "1-on-1 AI sessions", "Custom meal plans"]
    },
    "premium": {
        "name": "Premium Wellness Plan",
        "amount": 39.99,
        "currency": "usd", 
        "description": "Complete wellness ecosystem with unlimited access",
        "features": ["All plus features", "Live coaching sessions", "Unlimited programs", "Priority support"]
    },
    "corporate": {
        "name": "Corporate Wellness Package",
        "amount": 99.99,
        "currency": "usd",
        "description": "Complete corporate wellness solution",
        "features": ["All premium features", "HR dashboard", "Team analytics", "Custom branding"]
    }
}

def get_stripe_checkout(webhook_url: str):
    """Initialize Stripe checkout with webhook URL"""
    return StripeCheckout(api_key=STRIPE_API_KEY, webhook_url=webhook_url)

async def create_payment_transaction(
    session_id: str,
    amount: float,
    currency: str,
    user_id: Optional[str] = None,
    metadata: Optional[Dict[str, str]] = None,
    package_id: Optional[str] = None
):
    """Create payment transaction record"""
    payment_id = str(uuid.uuid4())
    
    transaction_data = {
        "_id": payment_id,
        "payment_id": payment_id,
        "session_id": session_id,
        "user_id": user_id,
        "amount": amount,
        "currency": currency,
        "package_id": package_id,
        "metadata": metadata or {},
        "payment_status": "pending",
        "status": "initiated",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    await payment_transactions_collection.insert_one(transaction_data)
    return payment_id

@router.get("/packages")
async def get_wellness_packages():
    """Get available wellness packages"""
    return {
        "packages": WELLNESS_PACKAGES,
        "currency": "usd"
    }

@router.post("/checkout/session", response_model=PaymentResponse)
async def create_checkout_session(request: PaymentRequest, http_request: Request):
    """Create Stripe checkout session for wellness package"""
    try:
        # Validate package
        if request.package_id not in WELLNESS_PACKAGES:
            raise HTTPException(status_code=400, detail="Invalid package selected")
        
        package = WELLNESS_PACKAGES[request.package_id]
        
        # Get amount from server-side package definition (security)
        amount = package["amount"]
        currency = package["currency"]
        
        # Construct webhook URL
        host_url = str(http_request.base_url).rstrip('/')
        webhook_url = f"{host_url}/api/payments/webhook/stripe"
        
        # Initialize Stripe checkout
        stripe_checkout = get_stripe_checkout(webhook_url)
        
        # Build success and cancel URLs
        success_url = f"{request.origin_url}/payment/success?session_id={{CHECKOUT_SESSION_ID}}"
        cancel_url = f"{request.origin_url}/payment/cancel"
        
        # Create checkout session
        checkout_request = CheckoutSessionRequest(
            amount=amount,
            currency=currency,
            success_url=success_url,
            cancel_url=cancel_url,
            metadata={
                "package_id": request.package_id,
                "user_id": request.user_id or "anonymous",
                "source": "team_welly_app"
            }
        )
        
        session: CheckoutSessionResponse = await stripe_checkout.create_checkout_session(checkout_request)
        
        # Create payment transaction record
        payment_id = await create_payment_transaction(
            session_id=session.session_id,
            amount=amount,
            currency=currency,
            user_id=request.user_id,
            metadata=checkout_request.metadata,
            package_id=request.package_id
        )
        
        return PaymentResponse(
            checkout_url=session.url,
            session_id=session.session_id,
            payment_id=payment_id
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Checkout session creation failed: {str(e)}")

@router.post("/checkout/custom", response_model=PaymentResponse)
async def create_custom_checkout_session(request: CustomPaymentRequest, http_request: Request):
    """Create custom amount checkout session"""
    try:
        # Validate amount
        if request.amount <= 0:
            raise HTTPException(status_code=400, detail="Amount must be greater than 0")
        
        # Construct webhook URL
        host_url = str(http_request.base_url).rstrip('/')
        webhook_url = f"{host_url}/api/payments/webhook/stripe"
        
        # Initialize Stripe checkout
        stripe_checkout = get_stripe_checkout(webhook_url)
        
        # Build success and cancel URLs
        success_url = f"{request.origin_url}/payment/success?session_id={{CHECKOUT_SESSION_ID}}"
        cancel_url = f"{request.origin_url}/payment/cancel"
        
        # Create checkout session
        checkout_request = CheckoutSessionRequest(
            amount=request.amount,
            currency=request.currency,
            success_url=success_url,
            cancel_url=cancel_url,
            metadata={
                "user_id": request.user_id or "anonymous",
                "source": "team_welly_app",
                "type": "custom_amount",
                **(request.metadata or {})
            }
        )
        
        session: CheckoutSessionResponse = await stripe_checkout.create_checkout_session(checkout_request)
        
        # Create payment transaction record
        payment_id = await create_payment_transaction(
            session_id=session.session_id,
            amount=request.amount,
            currency=request.currency,
            user_id=request.user_id,
            metadata=checkout_request.metadata
        )
        
        return PaymentResponse(
            checkout_url=session.url,
            session_id=session.session_id,
            payment_id=payment_id
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Custom checkout session creation failed: {str(e)}")

@router.get("/checkout/status/{session_id}")
async def get_checkout_status(session_id: str, http_request: Request):
    """Get checkout session status and update payment transaction"""
    try:
        # Construct webhook URL
        host_url = str(http_request.base_url).rstrip('/')
        webhook_url = f"{host_url}/api/payments/webhook/stripe"
        
        # Initialize Stripe checkout
        stripe_checkout = get_stripe_checkout(webhook_url)
        
        # Get status from Stripe
        checkout_status: CheckoutStatusResponse = await stripe_checkout.get_checkout_status(session_id)
        
        # Find payment transaction
        transaction = await payment_transactions_collection.find_one({"session_id": session_id})
        
        if transaction:
            # Update transaction status if it has changed
            if (transaction["payment_status"] != checkout_status.payment_status or 
                transaction["status"] != checkout_status.status):
                
                await payment_transactions_collection.update_one(
                    {"session_id": session_id},
                    {
                        "$set": {
                            "payment_status": checkout_status.payment_status,
                            "status": checkout_status.status,
                            "amount_total": checkout_status.amount_total,
                            "currency": checkout_status.currency,
                            "updated_at": datetime.utcnow()
                        }
                    }
                )
                
                # If payment successful, perform post-payment actions
                if checkout_status.payment_status == "paid" and transaction["payment_status"] != "paid":
                    await process_successful_payment(transaction)
        
        return {
            "session_id": session_id,
            "status": checkout_status.status,
            "payment_status": checkout_status.payment_status,
            "amount_total": checkout_status.amount_total,
            "currency": checkout_status.currency,
            "metadata": checkout_status.metadata
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Status check failed: {str(e)}")

async def process_successful_payment(transaction: dict):
    """Process successful payment (upgrade user plan, etc.)"""
    try:
        user_id = transaction.get("user_id")
        package_id = transaction.get("package_id")
        
        if user_id and user_id != "anonymous" and package_id:
            # Update user plan
            await users_collection.update_one(
                {"_id": user_id},
                {
                    "$set": {
                        "plan": package_id,
                        "plan_upgraded_at": datetime.utcnow(),
                        "subscription_status": "active"
                    }
                }
            )
            
            print(f"✅ User {user_id} upgraded to {package_id} plan")
        
    except Exception as e:
        print(f"❌ Error processing successful payment: {str(e)}")

@router.post("/webhook/stripe")
async def stripe_webhook(request: Request):
    """Handle Stripe webhook events"""
    try:
        body = await request.body()
        stripe_signature = request.headers.get("Stripe-Signature")
        
        # Construct webhook URL
        host_url = str(request.base_url).rstrip('/')
        webhook_url = f"{host_url}/api/payments/webhook/stripe"
        
        # Initialize Stripe checkout
        stripe_checkout = get_stripe_checkout(webhook_url)
        
        # Handle webhook
        webhook_response = await stripe_checkout.handle_webhook(body, stripe_signature)
        
        # Process webhook event
        if webhook_response.event_type == "checkout.session.completed":
            session_id = webhook_response.session_id
            
            # Update transaction status
            await payment_transactions_collection.update_one(
                {"session_id": session_id},
                {
                    "$set": {
                        "payment_status": webhook_response.payment_status,
                        "webhook_received_at": datetime.utcnow(),
                        "updated_at": datetime.utcnow()
                    }
                }
            )
            
            # Get transaction for post-processing
            transaction = await payment_transactions_collection.find_one({"session_id": session_id})
            if transaction and webhook_response.payment_status == "paid":
                await process_successful_payment(transaction)
        
        return {"status": "success", "event_type": webhook_response.event_type}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Webhook processing failed: {str(e)}")

@router.get("/history")
async def get_payment_history(user_id: str):
    """Get payment history for user"""
    try:
        # Get payment transactions for user
        transactions = await payment_transactions_collection.find(
            {"user_id": user_id}
        ).sort("created_at", -1).limit(50).to_list(length=50)
        
        return {"transactions": transactions}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Payment history retrieval failed: {str(e)}")

@router.get("/transaction/{payment_id}")
async def get_payment_transaction(payment_id: str):
    """Get specific payment transaction"""
    try:
        transaction = await payment_transactions_collection.find_one({"payment_id": payment_id})
        
        if not transaction:
            raise HTTPException(status_code=404, detail="Transaction not found")
        
        return transaction
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Transaction retrieval failed: {str(e)}")

# Demo endpoints
@router.post("/demo/success")
async def demo_payment_success():
    """Demo successful payment for testing"""
    return {
        "status": "success",
        "message": "Payment completed successfully!",
        "transaction_id": "demo-transaction-123",
        "amount": 19.99,
        "currency": "usd"
    }

@router.get("/demo/packages")
async def demo_packages_info():
    """Demo endpoint showing package information"""
    return {
        "message": "Stripe integration is configured and ready!",
        "packages": WELLNESS_PACKAGES,
        "stripe_configured": bool(STRIPE_API_KEY and STRIPE_API_KEY != "sk_test_demo_key"),
        "features": [
            "✅ Secure payment processing",
            "✅ Multiple wellness packages",
            "✅ Automatic plan upgrades",
            "✅ Payment history tracking",
            "✅ Webhook event handling"
        ]
    }