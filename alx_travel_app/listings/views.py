"""
Views for the listings app.
"""
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .models import Listing, ListingImage, Booking, Review
from .serializers import ListingSerializer, ListingImageSerializer, BookingSerializer, ReviewSerializer


class ListingViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing listings
    """
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)  # Fixed: should be owner, not reviewer
    
    def get_queryset(self):
        """
        Optionally restricts the returned listings by filtering
        against query parameters in the URL.
        """
        queryset = Listing.objects.filter(is_active=True)
        
        # Filter by listing type
        listing_type = self.request.query_params.get('type')
        if listing_type:
            queryset = queryset.filter(listing_type=listing_type)
            
        # Filter by location
        location = self.request.query_params.get('location')
        if location:
            queryset = queryset.filter(location__icontains=location)
            
        # Filter by price range
        min_price = self.request.query_params.get('min_price')
        if min_price:
            queryset = queryset.filter(price_per_night__gte=min_price)
            
        max_price = self.request.query_params.get('max_price')
        if max_price:
            queryset = queryset.filter(price_per_night__lte=max_price)
            
        # Filter by number of guests
        guests = self.request.query_params.get('guests')
        if guests:
            queryset = queryset.filter(max_guests__gte=guests)
            
        # Search functionality
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(location__icontains=search)
            )
            
        return queryset
    
    def perform_update(self, serializer):
        """Only allow owners to update their own listings"""
        if serializer.instance.owner != self.request.user:
            return Response(
                {'error': 'You can only update your own listings'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        serializer.save()
    
    def perform_destroy(self, instance):
        """Only allow owners to delete their own listings"""
        if instance.owner != self.request.user:
            return Response(
                {'error': 'You can only delete your own listings'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        instance.delete()
    
    @action(detail=True, methods=['get'])
    def reviews(self, request, pk=None):
        """Get all reviews for a specific listing"""
        listing = self.get_object()
        reviews = listing.reviews.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def bookings(self, request, pk=None):
        """Get all bookings for a specific listing (owner only)"""
        listing = self.get_object()
        if request.user != listing.owner:
            return Response(
                {'error': 'Permission denied'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        bookings = listing.bookings.all()
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)


class ListingImageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing listing images
    """
    queryset = ListingImage.objects.all()
    serializer_class = ListingImageSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def perform_create(self, serializer):
        listing_id = self.request.data.get('listing')
        serializer.save(listing_id=listing_id)


class BookingViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing bookings
    """
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(guest=self.request.user)
    
    def get_queryset(self):
        """
        Users can only see their own bookings (as guest) or bookings for their listings (as owner)
        """
        # Handle Swagger schema generation
        if getattr(self, 'swagger_fake_view', False):
            return Booking.objects.none()
        
        # Handle unauthenticated users
        if not self.request.user.is_authenticated:
            return Booking.objects.none()
        
        user = self.request.user
        return Booking.objects.filter(
            Q(guest=user) | Q(listing__owner=user)
        ).distinct()
    
    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        """Update booking status (owner only)"""
        booking = self.get_object()
        
        # Only listing owner can update booking status
        if request.user != booking.listing.owner:
            return Response(
                {'error': 'Only listing owner can update booking status'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        new_status = request.data.get('status')
        if new_status not in ['pending', 'confirmed', 'cancelled', 'completed']:
            return Response(
                {'error': 'Invalid status'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        booking.status = new_status
        booking.save()
        
        serializer = BookingSerializer(booking)
        return Response(serializer.data)

class ReviewViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing reviews
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(reviewer=self.request.user)
    
    def get_queryset(self):
        """
        Filter reviews by listing if specified
        """
        queryset = Review.objects.all()
        listing_id = self.request.query_params.get('listing')
        if listing_id:
            queryset = queryset.filter(listing_id=listing_id)
        return queryset
    
    def perform_update(self, serializer):
        """Only allow users to update their own reviews"""
        if serializer.instance.reviewer != self.request.user:
            return Response(
                {'error': 'You can only update your own reviews'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        serializer.save()
    
    def perform_destroy(self, instance):
        """Only allow users to delete their own reviews"""
        if instance.reviewer != self.request.user:
            return Response(
                {'error': 'You can only delete your own reviews'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        instance.delete()