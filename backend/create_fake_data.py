from faker import Faker
from models.user import User
from models import storage
import random
from datetime import datetime
from models.cohort import Cohort
fake = Faker()
# If u want the fake data to be location specific
# use this:
# fake = Faker('ja_JP') 🌚 -- maybe Uchiha Itachi will pop up
# sadly Nigeria unavailable 😮‍💨


def create_fake_users():
    users = []
    for _ in range(30):
        total_seconds = random.randint(0, 1000000)
        daily_average = total_seconds // 7
        end_date = datetime.datetime.now() + datetime.timedelta(days=90)
        user = User(
            name=fake.name(),
            photo_url=fake.image_url(),
            username=fake.user_name(),
            twitter_username=fake.user_name(),
            whatsapp=fake.phone_number(),
            email=fake.email(),
            github_uid=fake.random_int(),
            wakatime_uid=str(fake.uuid4()),
            gh_access_token=str(fake.uuid4()),
            wk_access_token=str(fake.uuid4()),
            wk_refresh_token=str(fake.uuid4()),
            waka_token_expires=fake.date_time_between(
                start_date=datetime.now(), end_date=end_date),
            waka_week_total_seconds=total_seconds,
            waka_week_daily_average=daily_average,
            likes_interests=' '.join(fake.words()),
            most_active_time=fake.random_element(
                elements=('morning', 'afternoon', 'evening', 'night')),
            timezone=fake.timezone(),
            github_session=str(fake.uuid4()),
            waka_session=str(fake.uuid4()),
            github_login=fake.user_name(),
            wakatime_login=fake.user_name(),
            requested_partners=fake.random_int(
                min=0, max=3),
        )
        user.save()
        users.append(user)
    return users


def create_fake_cohorts():
    create_fake_users()
    users = list(storage.all(User).values())
    existing_cohorts = storage.all(Cohort).values()
    for i in range(8, 15):
        cohort = next((c for c in existing_cohorts if c.number == i), None)
        if cohort is None:
            cohort_users = random.sample(
                users, k=random.randint(1, len(users)))
            cohort = Cohort(
                name=fake.word(),
                number=i,
                users=cohort_users
            )
            cohort.save()
        else:
            cohort.users.extend(random.sample(
                users, k=random.randint(1, len(users))))
            cohort.save()


create_fake_cohorts()
