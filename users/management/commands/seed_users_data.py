from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from users.models import User, Profile
import random


class Command(BaseCommand):
    help = 'Seed the database with sample user and profile data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing user data before seeding',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting to seed user data...'))

        # Clear existing data if requested
        if options['clear']:
            # Delete profiles first (due to foreign key relationship)
            Profile.objects.filter(user__is_superuser=False).delete()
            User.objects.filter(is_superuser=False).delete()
            self.stdout.write(self.style.WARNING('Cleared existing user data (preserved superusers)'))

        # Sample user data
        sample_users = [
            {
                'username': 'pilot_ahmet',
                'email': 'ahmet.yilmaz@airline.com',
                'first_name': 'Ahmet',
                'last_name': 'Yılmaz',
                'role': 'staff',
                'bio': 'Senior pilot with 15 years of experience in commercial aviation.',
                'is_verified': True
            },
            {
                'username': 'pilot_mehmet',
                'email': 'mehmet.kaya@airline.com',
                'first_name': 'Mehmet',
                'last_name': 'Kaya',
                'role': 'staff',
                'bio': 'Experienced pilot specializing in international flights.',
                'is_verified': True
            },
            {
                'username': 'crew_ayse',
                'email': 'ayse.celik@airline.com',
                'first_name': 'Ayşe',
                'last_name': 'Çelik',
                'role': 'staff',
                'bio': 'Flight attendant with excellent customer service skills.',
                'is_verified': True
            },
            {
                'username': 'crew_fatma',
                'email': 'fatma.arslan@airline.com',
                'first_name': 'Fatma',
                'last_name': 'Arslan',
                'role': 'staff',
                'bio': 'Senior cabin crew member and safety specialist.',
                'is_verified': True
            },
            {
                'username': 'admin_user',
                'email': 'admin@airline.com',
                'first_name': 'Admin',
                'last_name': 'User',
                'role': 'admin',
                'bio': 'System administrator managing flight operations.',
                'is_verified': True
            },
            {
                'username': 'manager_ali',
                'email': 'ali.demir@airline.com',
                'first_name': 'Ali',
                'last_name': 'Demir',
                'role': 'admin',
                'bio': 'Flight operations manager overseeing daily operations.',
                'is_verified': True
            },
            {
                'username': 'viewer_john',
                'email': 'john.doe@airline.com',
                'first_name': 'John',
                'last_name': 'Doe',
                'role': 'viewer',
                'bio': 'Operations analyst monitoring flight schedules.',
                'is_verified': False
            },
            {
                'username': 'viewer_jane',
                'email': 'jane.smith@airline.com',
                'first_name': 'Jane',
                'last_name': 'Smith',
                'role': 'viewer',
                'bio': 'Customer service representative tracking flight status.',
                'is_verified': False
            },
            {
                'username': 'guest_user',
                'email': 'guest@airline.com',
                'first_name': 'Guest',
                'last_name': 'User',
                'role': 'viewer',
                'bio': 'Temporary access user for demonstrations.',
                'is_verified': False
            },
            {
                'username': 'trainee_seda',
                'email': 'seda.aydin@airline.com',
                'first_name': 'Seda',
                'last_name': 'Aydın',
                'role': 'viewer',
                'bio': 'Flight operations trainee learning the system.',
                'is_verified': True
            }
        ]

        # Additional random users for variety
        turkish_first_names = [
            'Emre', 'Zeynep', 'Burak', 'Elif', 'Cem', 'Deniz', 'Murat', 'Selin',
            'Özge', 'Berk', 'Merve', 'Kerem', 'Pınar', 'Tolga', 'Gamze'
        ]
        
        turkish_last_names = [
            'Özkan', 'Güneş', 'Aydın', 'Koç', 'Şen', 'Yurt', 'Polat', 'Tekin',
            'Akın', 'Doğan', 'Yıldız', 'Taş', 'Öz', 'Er', 'Kurt'
        ]

        domains = ['airline.com', 'flightops.com', 'aviation.com']
        roles = ['viewer', 'staff', 'admin']
        
        # Generate additional random users
        for i in range(15):
            first_name = random.choice(turkish_first_names)
            last_name = random.choice(turkish_last_names)
            username = f"{first_name.lower()}_{last_name.lower()}_{i+1}"
            email = f"{first_name.lower()}.{last_name.lower()}{i+1}@{random.choice(domains)}"
            role = random.choice(roles)
            
            sample_users.append({
                'username': username,
                'email': email,
                'first_name': first_name,
                'last_name': last_name,
                'role': role,
                'bio': f'{role.title()} user with diverse experience in aviation industry.',
                'is_verified': random.choice([True, False])
            })

        # Create users and profiles
        created_users = 0
        created_profiles = 0
        
        for user_data in sample_users:
            # Check if user already exists
            if User.objects.filter(username=user_data['username']).exists():
                self.stdout.write(f"User {user_data['username']} already exists, skipping...")
                continue
                
            # Create user (Profile will be created automatically via signal)
            user = User.objects.create(
                username=user_data['username'],
                email=user_data['email'],
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                role=user_data['role'],
                password=make_password('password123'),  # Default password for all users
                is_active=True
            )
            created_users += 1
            
            # Update profile with additional data
            profile = user.profile
            profile.bio = user_data['bio']
            profile.is_verified = user_data['is_verified']
            profile.save()
            created_profiles += 1

        self.stdout.write(self.style.SUCCESS(f'Created {created_users} users'))
        self.stdout.write(self.style.SUCCESS(f'Created {created_profiles} profiles'))
        
        # Display summary
        self.stdout.write(self.style.SUCCESS('User seed data creation completed!'))
        self.stdout.write(f'Total users: {User.objects.count()}')
        self.stdout.write(f'Total profiles: {Profile.objects.count()}')
        
        # Display role distribution
        self.stdout.write(self.style.WARNING('\nUser role distribution:'))
        for role in ['viewer', 'staff', 'admin']:
            count = User.objects.filter(role=role).count()
            self.stdout.write(f'  {role.capitalize()}: {count} users')
        
        # Display some sample users
        self.stdout.write(self.style.WARNING('\nSample users created:'))
        for user in User.objects.all()[:10]:
            verified_status = "✓" if user.profile.is_verified else "✗"
            self.stdout.write(f'  {user.username} ({user.role}) - {user.email} [{verified_status}]')
            
        self.stdout.write(self.style.SUCCESS('\nDefault password for all users: password123'))
