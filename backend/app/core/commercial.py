"""
HireSense AI - Commercial Architecture & Subscription Quotas (Phase 13)
Cleanly defines tiers, feature limits, and quota enforcement hooks
WITHOUT activating any live payment gateway or billing charges.
"""

from typing import Dict, Any, Optional
from enum import Enum


class SubscriptionPlan(str, Enum):
    CANDIDATE_FREE = "candidate_free"
    RECRUITER_FREE = "recruiter_free"
    RECRUITER_PRO = "recruiter_pro"
    ENTERPRISE = "enterprise"


TIER_LIMITS: Dict[SubscriptionPlan, Dict[str, Any]] = {
    SubscriptionPlan.CANDIDATE_FREE: {
        "max_cvs": 5,
        "ai_match_per_day": 50,
        "can_export_data": True,
        "can_delete_data": True,
    },
    SubscriptionPlan.RECRUITER_FREE: {
        "max_active_jobs": 3,
        "max_applications_per_month": 50,
        "ai_ranking_enabled": True,
        "team_members_limit": 1,
        "advanced_analytics": False,
        "priority_support": False
    },
    SubscriptionPlan.RECRUITER_PRO: {
        "max_active_jobs": 25,
        "max_applications_per_month": 500,
        "ai_ranking_enabled": True,
        "team_members_limit": 5,
        "advanced_analytics": True,
        "priority_support": True
    },
    SubscriptionPlan.ENTERPRISE: {
        "max_active_jobs": 9999,
        "max_applications_per_month": 99999,
        "ai_ranking_enabled": True,
        "team_members_limit": 50,
        "advanced_analytics": True,
        "priority_support": True,
        "custom_sla": True
    }
}


def can_post_job(current_active_jobs: int, plan: SubscriptionPlan = SubscriptionPlan.RECRUITER_FREE) -> bool:
    """Checks whether the company can publish an additional job posting under current quota."""
    limits = TIER_LIMITS.get(plan, TIER_LIMITS[SubscriptionPlan.RECRUITER_FREE])
    return current_active_jobs < limits["max_active_jobs"]


def can_add_team_member(current_member_count: int, plan: SubscriptionPlan = SubscriptionPlan.RECRUITER_FREE) -> bool:
    """Checks whether additional recruiter team members can be added under company quota."""
    limits = TIER_LIMITS.get(plan, TIER_LIMITS[SubscriptionPlan.RECRUITER_FREE])
    return current_member_count < limits["team_members_limit"]

