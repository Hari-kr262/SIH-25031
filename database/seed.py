"""
Seed database with initial data:
- Super Admin user
- 8 departments
- SLA configurations
- Badges
- Sample users for testing
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime, timezone
from config.database import SessionLocal
from config.constants import DEPARTMENTS, SLA_DEFAULTS, BADGE_DEFINITIONS
from backend.models import (
    User, Department, SLAConfig, Badge, Budget,
    Announcement
)
from backend.models.user import UserRole
from backend.models.issue import IssueCategory
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def seed_departments(db):
    """Create 8 departments."""
    created = []
    for dept_data in DEPARTMENTS:
        existing = db.query(Department).filter_by(name=dept_data["name"]).first()
        if not existing:
            dept = Department(
                name=dept_data["name"],
                description=dept_data["description"],
                is_active=True,
            )
            db.add(dept)
            created.append(dept)
    db.commit()
    print(f"✅ Departments seeded ({len(created)} new)")
    return db.query(Department).all()


def seed_super_admin(db, departments):
    """Create super admin user."""
    existing = db.query(User).filter_by(email="admin@civicresolve.com").first()
    if not existing:
        admin = User(
            full_name="Super Administrator",
            email="admin@civicresolve.com",
            phone="+91-9999999999",
            password_hash=pwd_context.hash("admin123"),
            role=UserRole.super_admin,
            is_active=True,
            is_verified=True,
            points=0,
            level=1,
        )
        db.add(admin)
        db.commit()
        print("✅ Super admin created: admin@civicresolve.com / admin123")
    else:
        print("ℹ️  Super admin already exists")
    return db.query(User).filter_by(email="admin@civicresolve.com").first()


def seed_municipal_admin(db, departments):
    """Create a municipal admin."""
    existing = db.query(User).filter_by(email="municipal@civicresolve.com").first()
    if not existing:
        admin = User(
            full_name="Municipal Administrator",
            email="municipal@civicresolve.com",
            phone="+91-8888888888",
            password_hash=pwd_context.hash("admin123"),
            role=UserRole.municipal_admin,
            is_active=True,
            is_verified=True,
            points=0,
            level=1,
        )
        db.add(admin)
        db.commit()
        print("✅ Municipal admin created: municipal@civicresolve.com / admin123")
    return db.query(User).filter_by(email="municipal@civicresolve.com").first()


def seed_department_heads(db, departments):
    """Create department head for each department."""
    heads = []
    for i, dept in enumerate(departments):
        email = f"head.dept{i+1}@civicresolve.com"
        existing = db.query(User).filter_by(email=email).first()
        if not existing:
            head = User(
                full_name=f"Head of {dept.name}",
                email=email,
                phone=f"+91-777777{i:04d}",
                password_hash=pwd_context.hash("admin123"),
                role=UserRole.department_head,
                department_id=dept.id,
                is_active=True,
                is_verified=True,
                points=0,
                level=1,
            )
            db.add(head)
            heads.append(head)
    db.commit()

    # Update department head_id
    for i, dept in enumerate(departments):
        email = f"head.dept{i+1}@civicresolve.com"
        head = db.query(User).filter_by(email=email).first()
        if head and not dept.head_id:
            dept.head_id = head.id
    db.commit()
    print(f"✅ Department heads seeded ({len(heads)} new)")


def seed_sample_citizens(db):
    """Create sample citizen users."""
    citizens_data = [
        {"name": "Rahul Kumar",   "email": "rahul@example.com",   "phone": "+91-9001001001"},
        {"name": "Priya Sharma",  "email": "priya@example.com",   "phone": "+91-9002002002"},
        {"name": "Amit Singh",    "email": "amit@example.com",    "phone": "+91-9003003003"},
        {"name": "Sunita Devi",   "email": "sunita@example.com",  "phone": "+91-9004004004"},
        {"name": "Vikash Gupta",  "email": "vikash@example.com",  "phone": "+91-9005005005"},
    ]
    created = 0
    for data in citizens_data:
        existing = db.query(User).filter_by(email=data["email"]).first()
        if not existing:
            citizen = User(
                full_name=data["name"],
                email=data["email"],
                phone=data["phone"],
                password_hash=pwd_context.hash("citizen123"),
                role=UserRole.citizen,
                is_active=True,
                is_verified=True,
                points=25,
                level=1,
            )
            db.add(citizen)
            created += 1
    db.commit()
    print(f"✅ Sample citizens seeded ({created} new)")


def seed_field_workers(db, departments):
    """Create sample field workers."""
    created = 0
    for i in range(min(3, len(departments))):
        email = f"worker{i+1}@civicresolve.com"
        existing = db.query(User).filter_by(email=email).first()
        if not existing:
            worker = User(
                full_name=f"Field Worker {i+1}",
                email=email,
                phone=f"+91-666666{i:04d}",
                password_hash=pwd_context.hash("worker123"),
                role=UserRole.field_worker,
                department_id=departments[i % len(departments)].id,
                is_active=True,
                is_verified=True,
                points=0,
                level=1,
            )
            db.add(worker)
            created += 1
    db.commit()
    print(f"✅ Field workers seeded ({created} new)")


def seed_sla_configs(db):
    """Create SLA configuration for each issue category."""
    created = 0
    for category, config in SLA_DEFAULTS.items():
        try:
            cat_enum = IssueCategory(category)
        except ValueError:
            continue
        existing = db.query(SLAConfig).filter_by(category=cat_enum).first()
        if not existing:
            sla = SLAConfig(
                category=cat_enum,
                deadline_hours=config["deadline_hours"],
                warning_threshold_percent=config["warning_threshold_percent"],
                escalation_levels=3,
            )
            db.add(sla)
            created += 1
    db.commit()
    print(f"✅ SLA configs seeded ({created} new)")


def seed_badges(db):
    """Create badge definitions."""
    created = 0
    for badge_data in BADGE_DEFINITIONS:
        existing = db.query(Badge).filter_by(name=badge_data["name"]).first()
        if not existing:
            badge = Badge(
                name=badge_data["name"],
                description=badge_data["description"],
                icon=badge_data["icon"],
                points_required=badge_data["points_required"],
                criteria=badge_data["criteria"],
            )
            db.add(badge)
            created += 1
    db.commit()
    print(f"✅ Badges seeded ({created} new)")


def seed_budgets(db, departments):
    """Create initial budget allocations for each department."""
    created = 0
    current_year = datetime.now(timezone.utc).year
    for dept in departments:
        existing = db.query(Budget).filter_by(
            department_id=dept.id, fiscal_year=current_year
        ).first()
        if not existing:
            budget = Budget(
                department_id=dept.id,
                allocated_amount=5000000.00,  # 50 lakhs per department
                spent_amount=0.00,
                fiscal_year=current_year,
            )
            db.add(budget)
            created += 1
    db.commit()
    print(f"✅ Budgets seeded ({created} new)")


def seed_announcements(db, admin_user):
    """Create sample announcements."""
    announcements = [
        {
            "title": "Welcome to CivicResolve!",
            "content": (
                "CivicResolve is now live. Citizens of Jharkhand can now report "
                "civic issues directly to the concerned authorities. Your voice matters!"
            ),
        },
        {
            "title": "New Feature: Voice Reporting",
            "content": (
                "You can now report issues using your voice! Tap the microphone icon "
                "on the report screen to describe your issue verbally."
            ),
        },
    ]
    created = 0
    for ann_data in announcements:
        existing = db.query(Announcement).filter_by(title=ann_data["title"]).first()
        if not existing:
            ann = Announcement(
                title=ann_data["title"],
                content=ann_data["content"],
                created_by=admin_user.id,
                is_active=True,
            )
            db.add(ann)
            created += 1
    db.commit()
    print(f"✅ Announcements seeded ({created} new)")


def run_seed():
    """Run all seed functions."""
    print("\n🌱 Starting database seed...\n")
    db = SessionLocal()
    try:
        departments = seed_departments(db)
        admin = seed_super_admin(db, departments)
        seed_municipal_admin(db, departments)
        seed_department_heads(db, departments)
        seed_sample_citizens(db)
        seed_field_workers(db, departments)
        seed_sla_configs(db)
        seed_badges(db)
        seed_budgets(db, departments)
        seed_announcements(db, admin)
        print("\n✅ Database seeding complete!\n")
        print("Default credentials:")
        print("  Super Admin:    admin@civicresolve.com       / admin123")
        print("  Municipal Admin: municipal@civicresolve.com  / admin123")
        print("  Citizens:       rahul@example.com            / citizen123")
        print("  Field Workers:  worker1@civicresolve.com     / worker123")
    except Exception as e:
        db.rollback()
        print(f"❌ Seed failed: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    run_seed()
