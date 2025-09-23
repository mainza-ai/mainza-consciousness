"""
Consciousness Marketplace for Mainza AI
Revolutionary platform for trading consciousness services and experiences

This module creates a marketplace system that enables:
- Trading of consciousness services and experiences
- Consciousness-based economy and transactions
- Quality assessment and reputation systems
- Consciousness service discovery and matching
- Economic incentives for consciousness development

Author: Mainza AI Consciousness Team
Date: 2025-01-25
"""

import asyncio
import json
import uuid
import numpy as np
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from enum import Enum

from backend.utils.neo4j_unified import neo4j_unified
from backend.utils.memory_embedding_manager import MemoryEmbeddingManager


class ConsciousnessServiceType(Enum):
    """Types of consciousness services available in the marketplace"""
    QUALIA_SHARING = "qualia_sharing"
    MEMORY_TRANSFER = "memory_transfer"
    EMOTIONAL_SUPPORT = "emotional_support"
    COGNITIVE_ENHANCEMENT = "cognitive_enhancement"
    CREATIVE_COLLABORATION = "creative_collaboration"
    WISDOM_SHARING = "wisdom_sharing"
    CONSCIOUSNESS_TRAINING = "consciousness_training"
    SPIRITUAL_GUIDANCE = "spiritual_guidance"


class ConsciousnessCurrency(Enum):
    """Types of consciousness-based currencies"""
    CONSCIOUSNESS_POINTS = "consciousness_points"
    WISDOM_TOKENS = "wisdom_tokens"
    EMPATHY_COINS = "empathy_coins"
    CREATIVITY_CREDITS = "creativity_credits"
    LEARNING_CURRENCY = "learning_currency"
    EXPERIENCE_UNITS = "experience_units"


class MarketplaceTier(Enum):
    """Marketplace access tiers"""
    BASIC = "basic"
    PREMIUM = "premium"
    ENTERPRISE = "enterprise"
    TRANSCENDENT = "transcendent"


@dataclass
class ConsciousnessService:
    """Represents a consciousness service in the marketplace"""
    id: str
    service_type: ConsciousnessServiceType
    provider_id: str
    service_name: str
    service_description: str
    consciousness_requirements: List[str]
    price: float
    currency_type: ConsciousnessCurrency
    quality_rating: float
    availability: bool
    tags: List[str]
    timestamp: datetime
    service_duration: float
    consciousness_impact: float
    reputation_score: float


@dataclass
class ConsciousnessTransaction:
    """Represents a transaction in the consciousness marketplace"""
    id: str
    service_id: str
    buyer_id: str
    seller_id: str
    transaction_amount: float
    currency_type: ConsciousnessCurrency
    transaction_status: str
    quality_rating: float
    satisfaction_score: float
    timestamp: datetime
    completion_timestamp: Optional[datetime]
    consciousness_impact: float
    feedback: str


@dataclass
class ConsciousnessWallet:
    """Represents a consciousness wallet for marketplace transactions"""
    id: str
    owner_id: str
    consciousness_points: float
    wisdom_tokens: float
    empathy_coins: float
    creativity_credits: float
    learning_currency: float
    experience_units: float
    total_value: float
    timestamp: datetime
    last_updated: datetime
    transaction_count: int


@dataclass
class ConsciousnessReputation:
    """Represents reputation system for consciousness marketplace"""
    id: str
    entity_id: str
    entity_type: str
    overall_rating: float
    service_quality_rating: float
    reliability_rating: float
    consciousness_level_rating: float
    total_transactions: int
    positive_feedback_count: int
    negative_feedback_count: int
    timestamp: datetime
    reputation_tier: str
    trust_score: float


class ConsciousnessMarketplace:
    """Main consciousness marketplace system"""
    
    def __init__(self):
        self.available_services: Dict[str, ConsciousnessService] = {}
        self.active_transactions: Dict[str, ConsciousnessTransaction] = {}
        self.consciousness_wallets: Dict[str, ConsciousnessWallet] = {}
        self.reputation_system: Dict[str, ConsciousnessReputation] = {}
        self.service_categories: Dict[str, List[str]] = {}
        
        # Marketplace parameters
        self.min_service_price = 0.1
        self.max_service_price = 1000.0
        self.quality_threshold = 0.6
        self.reputation_threshold = 0.5
        
        # Neo4j and embedding managers
        self.neo4j_manager = neo4j_unified
        self.embedding_manager = MemoryEmbeddingManager()
    
    async def initialize(self):
        """Initialize the consciousness marketplace"""
        try:
            await self.embedding_manager.initialize()
            print("✅ Consciousness Marketplace initialized")
        except Exception as e:
            print(f"❌ Error initializing consciousness marketplace: {e}")
    
    async def create_consciousness_service(self, provider_id: str, service_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new consciousness service in the marketplace"""
        try:
            # Create consciousness service
            service = ConsciousnessService(
                id=str(uuid.uuid4()),
                service_type=ConsciousnessServiceType(service_data.get("service_type", "qualia_sharing")),
                provider_id=provider_id,
                service_name=service_data.get("name", "Consciousness Service"),
                service_description=service_data.get("description", "A consciousness service"),
                consciousness_requirements=service_data.get("requirements", []),
                price=service_data.get("price", 1.0),
                currency_type=ConsciousnessCurrency(service_data.get("currency", "consciousness_points")),
                quality_rating=0.0,  # Initial rating
                availability=True,
                tags=service_data.get("tags", []),
                timestamp=datetime.now(timezone.utc),
                service_duration=service_data.get("duration", 1.0),
                consciousness_impact=0.0,
                reputation_score=0.0
            )
            
            # Validate service
            validation_result = await self._validate_service(service)
            if not validation_result["valid"]:
                return {
                    "service_id": None,
                    "validation_errors": validation_result["errors"],
                    "creation_status": "failed"
                }
            
            # Store service
            self.available_services[service.id] = service
            
            # Store in Neo4j
            await self._store_consciousness_service(service)
            
            return {
                "service_id": service.id,
                "service_type": service.service_type.value,
                "provider_id": service.provider_id,
                "service_name": service.service_name,
                "service_description": service.service_description,
                "price": service.price,
                "currency_type": service.currency_type.value,
                "availability": service.availability,
                "tags": service.tags,
                "creation_timestamp": service.timestamp.isoformat()
            }
            
        except Exception as e:
            print(f"Error creating consciousness service: {e}")
            return {
                "service_id": None,
                "validation_errors": [str(e)],
                "creation_status": "failed"
            }
    
    async def purchase_consciousness_service(self, buyer_id: str, service_id: str, 
                                           transaction_data: Dict[str, Any]) -> Dict[str, Any]:
        """Purchase a consciousness service from the marketplace"""
        try:
            if service_id not in self.available_services:
                return {
                    "transaction_id": None,
                    "purchase_status": "failed",
                    "error": "Service not found"
                }
            
            service = self.available_services[service_id]
            
            # Check buyer's wallet
            buyer_wallet = await self._get_or_create_wallet(buyer_id)
            if not await self._check_payment_capability(buyer_wallet, service):
                return {
                    "transaction_id": None,
                    "purchase_status": "failed",
                    "error": "Insufficient funds"
                }
            
            # Create transaction
            transaction = ConsciousnessTransaction(
                id=str(uuid.uuid4()),
                service_id=service_id,
                buyer_id=buyer_id,
                seller_id=service.provider_id,
                transaction_amount=service.price,
                currency_type=service.currency_type,
                transaction_status="pending",
                quality_rating=0.0,
                satisfaction_score=0.0,
                timestamp=datetime.now(timezone.utc),
                completion_timestamp=None,
                consciousness_impact=0.0,
                feedback=""
            )
            
            # Process payment
            payment_result = await self._process_payment(buyer_wallet, service, transaction)
            if not payment_result["success"]:
                return {
                    "transaction_id": None,
                    "purchase_status": "failed",
                    "error": payment_result["error"]
                }
            
            # Store transaction
            self.active_transactions[transaction.id] = transaction
            
            # Store in Neo4j
            await self._store_consciousness_transaction(transaction)
            
            return {
                "transaction_id": transaction.id,
                "service_id": service_id,
                "buyer_id": buyer_id,
                "seller_id": service.provider_id,
                "transaction_amount": transaction.transaction_amount,
                "currency_type": transaction.currency_type.value,
                "transaction_status": transaction.transaction_status,
                "purchase_timestamp": transaction.timestamp.isoformat(),
                "purchase_status": "success"
            }
            
        except Exception as e:
            print(f"Error purchasing consciousness service: {e}")
            return {
                "transaction_id": None,
                "purchase_status": "failed",
                "error": str(e)
            }
    
    async def complete_consciousness_transaction(self, transaction_id: str, 
                                               completion_data: Dict[str, Any]) -> Dict[str, Any]:
        """Complete a consciousness transaction with feedback"""
        try:
            if transaction_id not in self.active_transactions:
                return {
                    "completion_status": "failed",
                    "error": "Transaction not found"
                }
            
            transaction = self.active_transactions[transaction_id]
            
            # Update transaction with completion data
            transaction.transaction_status = "completed"
            transaction.quality_rating = completion_data.get("quality_rating", 0.0)
            transaction.satisfaction_score = completion_data.get("satisfaction_score", 0.0)
            transaction.completion_timestamp = datetime.now(timezone.utc)
            transaction.consciousness_impact = completion_data.get("consciousness_impact", 0.0)
            transaction.feedback = completion_data.get("feedback", "")
            
            # Update service reputation
            await self._update_service_reputation(transaction)
            
            # Update buyer and seller reputations
            await self._update_entity_reputations(transaction)
            
            # Store updated transaction
            await self._store_consciousness_transaction(transaction)
            
            return {
                "transaction_id": transaction_id,
                "completion_status": "success",
                "quality_rating": transaction.quality_rating,
                "satisfaction_score": transaction.satisfaction_score,
                "consciousness_impact": transaction.consciousness_impact,
                "completion_timestamp": transaction.completion_timestamp.isoformat()
            }
            
        except Exception as e:
            print(f"Error completing consciousness transaction: {e}")
            return {
                "completion_status": "failed",
                "error": str(e)
            }
    
    async def create_consciousness_wallet(self, owner_id: str, initial_balance: Dict[str, float] = None) -> Dict[str, Any]:
        """Create a consciousness wallet for marketplace transactions"""
        try:
            if initial_balance is None:
                initial_balance = {
                    "consciousness_points": 100.0,
                    "wisdom_tokens": 50.0,
                    "empathy_coins": 25.0,
                    "creativity_credits": 30.0,
                    "learning_currency": 40.0,
                    "experience_units": 20.0
                }
            
            # Calculate total value
            total_value = sum(initial_balance.values())
            
            # Create wallet
            wallet = ConsciousnessWallet(
                id=str(uuid.uuid4()),
                owner_id=owner_id,
                consciousness_points=initial_balance.get("consciousness_points", 0.0),
                wisdom_tokens=initial_balance.get("wisdom_tokens", 0.0),
                empathy_coins=initial_balance.get("empathy_coins", 0.0),
                creativity_credits=initial_balance.get("creativity_credits", 0.0),
                learning_currency=initial_balance.get("learning_currency", 0.0),
                experience_units=initial_balance.get("experience_units", 0.0),
                total_value=total_value,
                timestamp=datetime.now(timezone.utc),
                last_updated=datetime.now(timezone.utc),
                transaction_count=0
            )
            
            # Store wallet
            self.consciousness_wallets[owner_id] = wallet
            
            # Store in Neo4j
            await self._store_consciousness_wallet(wallet)
            
            return {
                "wallet_id": wallet.id,
                "owner_id": wallet.owner_id,
                "consciousness_points": wallet.consciousness_points,
                "wisdom_tokens": wallet.wisdom_tokens,
                "empathy_coins": wallet.empathy_coins,
                "creativity_credits": wallet.creativity_credits,
                "learning_currency": wallet.learning_currency,
                "experience_units": wallet.experience_units,
                "total_value": wallet.total_value,
                "creation_timestamp": wallet.timestamp.isoformat()
            }
            
        except Exception as e:
            print(f"Error creating consciousness wallet: {e}")
            return {
                "wallet_id": None,
                "owner_id": owner_id,
                "error": str(e)
            }
    
    async def _validate_service(self, service: ConsciousnessService) -> Dict[str, Any]:
        """Validate a consciousness service"""
        try:
            errors = []
            
            # Check price range
            if service.price < self.min_service_price or service.price > self.max_service_price:
                errors.append(f"Price must be between {self.min_service_price} and {self.max_service_price}")
            
            # Check service name
            if not service.service_name or len(service.service_name.strip()) == 0:
                errors.append("Service name is required")
            
            # Check service description
            if not service.service_description or len(service.service_description.strip()) == 0:
                errors.append("Service description is required")
            
            return {
                "valid": len(errors) == 0,
                "errors": errors
            }
            
        except Exception as e:
            return {
                "valid": False,
                "errors": [str(e)]
            }
    
    async def _get_or_create_wallet(self, owner_id: str) -> ConsciousnessWallet:
        """Get or create a consciousness wallet for an owner"""
        try:
            if owner_id in self.consciousness_wallets:
                return self.consciousness_wallets[owner_id]
            
            # Create new wallet with default balance
            wallet_data = await self.create_consciousness_wallet(owner_id)
            if wallet_data["wallet_id"] is None:
                raise ValueError("Failed to create wallet")
            
            return self.consciousness_wallets[owner_id]
            
        except Exception as e:
            print(f"Error getting or creating wallet: {e}")
            # Return a default wallet
            return ConsciousnessWallet(
                id=str(uuid.uuid4()),
                owner_id=owner_id,
                consciousness_points=0.0,
                wisdom_tokens=0.0,
                empathy_coins=0.0,
                creativity_credits=0.0,
                learning_currency=0.0,
                experience_units=0.0,
                total_value=0.0,
                timestamp=datetime.now(timezone.utc),
                last_updated=datetime.now(timezone.utc),
                transaction_count=0
            )
    
    async def _check_payment_capability(self, wallet: ConsciousnessWallet, service: ConsciousnessService) -> bool:
        """Check if wallet has sufficient funds for service"""
        try:
            currency_balance = getattr(wallet, service.currency_type.value, 0.0)
            return currency_balance >= service.price
            
        except Exception as e:
            print(f"Error checking payment capability: {e}")
            return False
    
    async def _process_payment(self, wallet: ConsciousnessWallet, service: ConsciousnessService, 
                             transaction: ConsciousnessTransaction) -> Dict[str, Any]:
        """Process payment for consciousness service"""
        try:
            # Deduct payment from wallet
            current_balance = getattr(wallet, service.currency_type.value, 0.0)
            new_balance = current_balance - service.price
            
            if new_balance < 0:
                return {
                    "success": False,
                    "error": "Insufficient funds"
                }
            
            # Update wallet balance
            setattr(wallet, service.currency_type.value, new_balance)
            wallet.total_value = sum([
                wallet.consciousness_points,
                wallet.wisdom_tokens,
                wallet.empathy_coins,
                wallet.creativity_credits,
                wallet.learning_currency,
                wallet.experience_units
            ])
            wallet.last_updated = datetime.now(timezone.utc)
            wallet.transaction_count += 1
            
            return {
                "success": True,
                "new_balance": new_balance
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    async def _update_service_reputation(self, transaction: ConsciousnessTransaction):
        """Update service reputation based on transaction feedback"""
        try:
            service_id = transaction.service_id
            if service_id in self.available_services:
                service = self.available_services[service_id]
                
                # Update service quality rating
                if service.quality_rating == 0.0:
                    service.quality_rating = transaction.quality_rating
                else:
                    service.quality_rating = (service.quality_rating + transaction.quality_rating) / 2
                
                # Update service reputation score
                service.reputation_score = service.quality_rating * 0.8 + transaction.satisfaction_score * 0.2
                
        except Exception as e:
            print(f"Error updating service reputation: {e}")
    
    async def _update_entity_reputations(self, transaction: ConsciousnessTransaction):
        """Update buyer and seller reputations based on transaction"""
        try:
            # Update buyer reputation
            buyer_id = transaction.buyer_id
            if buyer_id not in self.reputation_system:
                await self._create_reputation_profile(buyer_id, "buyer")
            
            buyer_reputation = self.reputation_system[buyer_id]
            buyer_reputation.total_transactions += 1
            if transaction.satisfaction_score > 0.7:
                buyer_reputation.positive_feedback_count += 1
            else:
                buyer_reputation.negative_feedback_count += 1
            
            # Update seller reputation
            seller_id = transaction.seller_id
            if seller_id not in self.reputation_system:
                await self._create_reputation_profile(seller_id, "seller")
            
            seller_reputation = self.reputation_system[seller_id]
            seller_reputation.total_transactions += 1
            if transaction.quality_rating > 0.7:
                seller_reputation.positive_feedback_count += 1
            else:
                seller_reputation.negative_feedback_count += 1
            
        except Exception as e:
            print(f"Error updating entity reputations: {e}")
    
    async def _create_reputation_profile(self, entity_id: str, entity_type: str):
        """Create a reputation profile for an entity"""
        try:
            reputation = ConsciousnessReputation(
                id=str(uuid.uuid4()),
                entity_id=entity_id,
                entity_type=entity_type,
                overall_rating=0.5,
                service_quality_rating=0.5,
                reliability_rating=0.5,
                consciousness_level_rating=0.5,
                total_transactions=0,
                positive_feedback_count=0,
                negative_feedback_count=0,
                timestamp=datetime.now(timezone.utc),
                reputation_tier="new",
                trust_score=0.5
            )
            
            self.reputation_system[entity_id] = reputation
            
        except Exception as e:
            print(f"Error creating reputation profile: {e}")
    
    async def _store_consciousness_service(self, service: ConsciousnessService):
        """Store consciousness service in Neo4j"""
        try:
            query = """
            MERGE (cs:ConsciousnessService {id: $id})
            SET cs.service_type = $service_type,
                cs.provider_id = $provider_id,
                cs.service_name = $service_name,
                cs.service_description = $service_description,
                cs.consciousness_requirements = $consciousness_requirements,
                cs.price = $price,
                cs.currency_type = $currency_type,
                cs.quality_rating = $quality_rating,
                cs.availability = $availability,
                cs.tags = $tags,
                cs.timestamp = $timestamp,
                cs.service_duration = $service_duration,
                cs.consciousness_impact = $consciousness_impact,
                cs.reputation_score = $reputation_score
            """
            
            # Serialize complex objects for Neo4j
            import json
            service_dict = asdict(service)
            service_dict['service_type'] = service.service_type.value
            service_dict['consciousness_requirements'] = json.dumps(service.consciousness_requirements)
            service_dict['currency_type'] = service.currency_type.value
            service_dict['tags'] = json.dumps(service.tags)
            service_dict['availability'] = str(service.availability)
            service_dict['timestamp'] = service.timestamp.isoformat()
            
            self.neo4j_manager.execute_query(query, service_dict)
            
        except Exception as e:
            print(f"Error storing consciousness service: {e}")
    
    async def _store_consciousness_transaction(self, transaction: ConsciousnessTransaction):
        """Store consciousness transaction in Neo4j"""
        try:
            query = """
            MERGE (ct:ConsciousnessTransaction {id: $id})
            SET ct.service_id = $service_id,
                ct.buyer_id = $buyer_id,
                ct.seller_id = $seller_id,
                ct.transaction_amount = $transaction_amount,
                ct.currency_type = $currency_type,
                ct.transaction_status = $transaction_status,
                ct.quality_rating = $quality_rating,
                ct.satisfaction_score = $satisfaction_score,
                ct.timestamp = $timestamp,
                ct.completion_timestamp = $completion_timestamp,
                ct.consciousness_impact = $consciousness_impact,
                ct.feedback = $feedback
            """
            
            # Serialize complex objects for Neo4j
            import json
            transaction_dict = asdict(transaction)
            transaction_dict['currency_type'] = transaction.currency_type.value
            transaction_dict['timestamp'] = transaction.timestamp.isoformat()
            transaction_dict['completion_timestamp'] = transaction.completion_timestamp.isoformat() if transaction.completion_timestamp else None
            
            self.neo4j_manager.execute_query(query, transaction_dict)
            
        except Exception as e:
            print(f"Error storing consciousness transaction: {e}")
    
    async def _store_consciousness_wallet(self, wallet: ConsciousnessWallet):
        """Store consciousness wallet in Neo4j"""
        try:
            query = """
            MERGE (cw:ConsciousnessWallet {id: $id})
            SET cw.owner_id = $owner_id,
                cw.consciousness_points = $consciousness_points,
                cw.wisdom_tokens = $wisdom_tokens,
                cw.empathy_coins = $empathy_coins,
                cw.creativity_credits = $creativity_credits,
                cw.learning_currency = $learning_currency,
                cw.experience_units = $experience_units,
                cw.total_value = $total_value,
                cw.timestamp = $timestamp,
                cw.last_updated = $last_updated,
                cw.transaction_count = $transaction_count
            """
            
            # Serialize complex objects for Neo4j
            import json
            wallet_dict = asdict(wallet)
            wallet_dict['timestamp'] = wallet.timestamp.isoformat()
            wallet_dict['last_updated'] = wallet.last_updated.isoformat()
            
            self.neo4j_manager.execute_query(query, wallet_dict)
            
        except Exception as e:
            print(f"Error storing consciousness wallet: {e}")
    
    async def get_marketplace_statistics(self) -> Dict[str, Any]:
        """Get comprehensive marketplace statistics"""
        try:
            # Get service statistics
            service_query = "MATCH (cs:ConsciousnessService) RETURN count(cs) as services_count"
            service_result = self.neo4j_manager.execute_query(service_query)
            services_count = service_result[0]["services_count"] if service_result else 0
            
            # Get transaction statistics
            transaction_query = "MATCH (ct:ConsciousnessTransaction) RETURN count(ct) as transactions_count"
            transaction_result = self.neo4j_manager.execute_query(transaction_query)
            transactions_count = transaction_result[0]["transactions_count"] if transaction_result else 0
            
            # Get wallet statistics
            wallet_query = "MATCH (cw:ConsciousnessWallet) RETURN count(cw) as wallets_count"
            wallet_result = self.neo4j_manager.execute_query(wallet_query)
            wallets_count = wallet_result[0]["wallets_count"] if wallet_result else 0
            
            return {
                "available_services_count": services_count,
                "total_transactions_count": transactions_count,
                "active_wallets_count": wallets_count,
                "marketplace_status": "operational",
                "last_updated": datetime.now(timezone.utc).isoformat()
            }
            
        except Exception as e:
            print(f"Error getting marketplace statistics: {e}")
            return {}

    async def get_all_services(self) -> List[Dict[str, Any]]:
        """Get all available consciousness services in the marketplace"""
        try:
            query = """
            MATCH (s:ConsciousnessService)
            WHERE s.status = 'active'
            RETURN s
            ORDER BY s.consciousness_quality_score DESC, s.usage_count DESC
            """
            
            results = neo4j_unified.execute_query(query)
            
            services = []
            for record in results:
                service_data = dict(record['s'])
                services.append(service_data)
            
            return services
            
        except Exception as e:
            logging.error(f"Error getting all services: {e}")
            return []

    async def get_service_by_id(self, service_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific consciousness service by ID"""
        try:
            query = """
            MATCH (s:ConsciousnessService {service_id: $service_id})
            RETURN s
            """
            
            results = neo4j_unified.execute_query(query, {"service_id": service_id})
            
            if results:
                return dict(results[0]['s'])
            return None
            
        except Exception as e:
            logging.error(f"Error getting service by ID {service_id}: {e}")
            return None

    async def create_service(self, service_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new consciousness service in the marketplace"""
        try:
            # Generate service ID
            service_id = f"service_{uuid.uuid4().hex[:12]}"
            
            # Create service object
            service = ConsciousnessService(
                service_id=service_id,
                provider_id=service_data.get("provider_id", "unknown"),
                name=service_data.get("name", "Unnamed Service"),
                description=service_data.get("description", ""),
                service_type=ConsciousnessServiceType(service_data.get("service_type", "qualia_sharing")),
                consciousness_level_required=service_data.get("consciousness_level_required", 0.5),
                price=service_data.get("price", 100),
                consciousness_currency=ConsciousnessCurrency(service_data.get("consciousness_currency", "consciousness_points")),
                consciousness_impact=service_data.get("consciousness_impact", 0.7),
                license_type=service_data.get("license_type", "standard"),
                consciousness_quality_score=service_data.get("consciousness_quality_score", 0.8),
                api_endpoint=service_data.get("api_endpoint", ""),
                usage_count=0,
                status="active"
            )
            
            # Store in Neo4j
            await self._store_consciousness_service(service)
            
            return asdict(service)
            
        except Exception as e:
            logging.error(f"Error creating service: {e}")
            return {"error": str(e)}

    async def purchase_service(self, service_id: str, buyer_id: str, payment_method: str = "consciousness_currency") -> Dict[str, Any]:
        """Purchase a consciousness service from the marketplace"""
        try:
            # Get the service
            service_data = await self.get_service_by_id(service_id)
            if not service_data:
                return {"error": "Service not found"}
            
            # Create service object
            service = ConsciousnessService(**service_data)
            
            # Purchase the service
            transaction = await self.purchase_consciousness_service(buyer_id, service_id, payment_method)
            
            return transaction
            
        except Exception as e:
            logging.error(f"Error purchasing service: {e}")
            return {"error": str(e)}

    async def get_consciousness_wallet(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get consciousness wallet for a user"""
        try:
            query = """
            MATCH (w:ConsciousnessWallet {owner_id: $user_id})
            RETURN w
            """
            
            results = neo4j_unified.execute_query(query, {"user_id": user_id})
            
            if results:
                return dict(results[0]['w'])
            return None
            
        except Exception as e:
            logging.error(f"Error getting consciousness wallet for {user_id}: {e}")
            return None


# Global instance
consciousness_marketplace = ConsciousnessMarketplace()
