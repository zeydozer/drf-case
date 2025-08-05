from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
  help = 'Seed all data (users, flights, and crew) for the application'

  def add_arguments(self, parser):
    parser.add_argument(
      '--clear',
      action='store_true',
      help='Clear existing data before seeding',
    )

  def handle(self, *args, **options):
    self.stdout.write(self.style.SUCCESS('Starting to seed all application data...'))
    
    clear_flag = '--clear' if options['clear'] else ''
    
    # Seed users first
    self.stdout.write(self.style.WARNING('1. Seeding users...'))
    try:
      if clear_flag:
        call_command('seed_users_data', '--clear')
      else:
        call_command('seed_users_data')
      self.stdout.write(self.style.SUCCESS('✓ Users seeded successfully'))
    except Exception as e:
      self.stdout.write(self.style.ERROR(f'✗ Failed to seed users: {e}'))
      return
    
    # Seed flights and crew
    self.stdout.write(self.style.WARNING('2. Seeding flights and crew...'))
    try:
      call_command('seed_data')
      self.stdout.write(self.style.SUCCESS('✓ Flights and crew seeded successfully'))
    except Exception as e:
      self.stdout.write(self.style.ERROR(f'✗ Failed to seed flights and crew: {e}'))
      return
    
    self.stdout.write(self.style.SUCCESS('\n🎉 All seed data creation completed successfully!'))
    self.stdout.write(self.style.SUCCESS('You can now use the application with sample data.'))
    
    # Display summary
    from users.models import User, Profile
    from flights.models import Flight
    from crew.models import CrewMember
    
    self.stdout.write(self.style.WARNING('\n📊 Data Summary:'))
    self.stdout.write(f'   Users: {User.objects.count()}')
    self.stdout.write(f'   Profiles: {Profile.objects.count()}')
    self.stdout.write(f'   Flights: {Flight.objects.count()}')
    self.stdout.write(f'   Crew Members: {CrewMember.objects.count()}')
    
    self.stdout.write(self.style.WARNING('\n🔐 Login Information:'))
    self.stdout.write('   Default password for all users: password123')
    self.stdout.write('   Sample usernames: pilot_ahmet, admin_user, viewer_john, etc.')
    self.stdout.write('\n   Use these credentials to test different user roles!')
