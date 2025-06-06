# ALX Travel App

A Django REST API for a travel booking application that allows users to list properties, make bookings, and leave reviews.

## Features

- **Listings Management**: Create, view, update, and delete travel property listings
- **Booking System**: Users can book properties with date validation and capacity checks
- **Review System**: Guests can leave reviews and ratings for properties they've stayed at
- **Image Upload**: Support for multiple images per listing
- **Advanced Filtering**: Filter listings by type, location, price range, and guest capacity
- **Search Functionality**: Search listings by title, description, or location
- **User Authentication**: JWT-based authentication for secure API access

## Models

### Listing
- Properties available for booking (hotels, apartments, villas, etc.)
- Includes pricing, capacity, location, and amenities information
- Belongs to an owner (User)

### Booking
- Represents a reservation for a specific listing
- Includes check-in/out dates, guest count, and booking status
- Automatic total price calculation based on nightly rate
- Status tracking (pending, confirmed, cancelled, completed)

### Review
- User reviews and ratings for listings
- Linked to bookings for verified stays
- Prevents listing owners from reviewing their own properties
- One review per user per listing

### ListingImage
- Multiple images per listing with primary image designation
- Image upload functionality with captions

## API Endpoints

### Listings
- `GET /api/listings/` - List all active listings
- `POST /api/listings/` - Create a new listing (authenticated users)
- `GET /api/listings/{id}/` - Get listing details
- `PUT/PATCH /api/listings/{id}/` - Update listing (owner only)
- `DELETE /api/listings/{id}/` - Delete listing (owner only)
- `GET /api/listings/{id}/reviews/` - Get all reviews for a listing
- `GET /api/listings/{id}/bookings/` - Get all bookings for a listing (owner only)

### Bookings
- `GET /api/bookings/` - List user's bookings (as guest or listing owner)
- `POST /api/bookings/` - Create a new booking
- `GET /api/bookings/{id}/` - Get booking details
- `PUT/PATCH /api/bookings/{id}/` - Update booking
- `DELETE /api/bookings/{id}/` - Cancel booking
- `PATCH /api/bookings/{id}/update_status/` - Update booking status (owner only)

### Reviews
- `GET /api/reviews/` - List all reviews
- `POST /api/reviews/` - Create a new review
- `GET /api/reviews/{id}/` - Get review details
- `PUT/PATCH /api/reviews/{id}/` - Update review (author only)
- `DELETE /api/reviews/{id}/` - Delete review (author only)

### Listing Images
- `GET /api/listing-images/` - List all images
- `POST /api/listing-images/` - Upload new image
- `GET /api/listing-images/{id}/` - Get image details
- `PUT/PATCH /api/listing-images/{id}/` - Update image
- `DELETE /api/listing-images/{id}/` - Delete image

## Query Parameters

### Listings
- `type` - Filter by listing type (hotel, apartment, villa, resort, hostel, other)
- `location` - Filter by location (case-insensitive partial match)
- `min_price` - Minimum price per night
- `max_price` - Maximum price per night
- `guests` - Minimum guest capacity
- `search` - Search in title, description, or location

### Reviews
- `listing` - Filter reviews by listing ID

## Setup Instructions

### Prerequisites
-Ensure you have the latest Python version installed For me, it's 3.12.4

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd alx_travel_app_0x00
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Seed the database (optional)**
   ```bash
   python manage.py seed
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

## Database Seeding

The project includes a management command to populate the database with sample data:

```bash
# Basic seeding with default counts
python manage.py seed

# Custom counts
python manage.py seed --listings 30 --bookings 100 --reviews 50

# Clear existing data before seeding
python manage.py seed --clear

# Help
python manage.py seed --help
```

### Seed Data Includes:
- **Users**: Sample hosts and guests with different roles
- **Listings**: Various property types in different locations
- **Bookings**: Sample reservations with different statuses
- **Reviews**: Ratings and comments for completed stays

## API Documentation

When running the development server, you can access:
- **Swagger UI**: http://localhost:8000/swagger/
- **ReDoc**: http://localhost:8000/redoc/

## Project Structure

```
alx_travel_app/
├── alx_travel_app/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── celery.py
├── listings/
│   ├── __init__.py
│   ├── models.py          # Database models
│   ├── serializers.py     # API serializers
│   ├── views.py           # API views
│   ├── urls.py            # URL routing
│   ├── admin.py           # Django admin configuration
│   ├── apps.py            # App configuration
│   └── management/
│       └── commands/
│           └── seed.py    # Database seeding command
├── media                 # Uploaded images
├── manage.py
└── README.md
```

## Data Validation

The application includes comprehensive data validation:

### Booking Validation
- Check-in date must be before check-out date
- Number of guests cannot exceed listing capacity
- Automatic total price calculation

### Review Validation
- Users cannot review their own listings
- One review per user per listing
- Rating must be between 1 and 5

### Business Logic
- Only listing owners can update booking status
- Users can only modify their own bookings and reviews
- Inactive listings are excluded from public listing views

## Authentication

The API uses Django's built-in authentication system. Most endpoints require authentication:
- **Read-only access**: Available to anonymous users for listings
- **Create/Update/Delete**: Requires authentication
- **Ownership checks**: Users can only modify their own content

## Error Handling

The API returns appropriate HTTP status codes and error messages:
- `400 Bad Request` - Validation errors
- `401 Unauthorized` - Authentication required
- `403 Forbidden` - Permission denied
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server errors

## Future Enhancements

- Payment integration
- Real-time notifications
- Advanced search with filters
- Booking calendar integration
- Email notifications
- Mobile app support
- Multi-language support
