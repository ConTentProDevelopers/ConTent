from django.contrib import admin
from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from testApp.models import MyUser
from testApp.models import Customer
from testApp.models import FieldOwner
from testApp.models import Campsite
from testApp.models import Rating
from testApp.models import Reservation
from testApp.models import PlaceType
from testApp.models import Place
from testApp.models import Convenience
from testApp.models import StaticPage

# Register your models here.


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = MyUser
        fields = ('email', 'first_name', 'last_name', 'phone_number')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = MyUser
        fields = ('email', 'password', 'first_name', 'last_name', 'phone_number', 'is_active', 'is_superuser')

    def clean_password(self):
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'first_name', 'last_name', 'phone_number', 'is_superuser')
    list_filter = ('is_superuser',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone_number')}),
        ('Permissions', {'fields': ('is_superuser',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'phone_number', 'password1', 'password2')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')
    list_filter = ()
    ordering = ('id',)
    filter_horizontal = ()


class FieldOwnerAdmin(admin.ModelAdmin):
    list_display = ('id', 'company_name', 'company_NIP', 'company_REGON', 'company_locality', 'company_address',
                    'company_postal_code', 'account_validated', 'user')
    list_filter = ()
    ordering = ('id',)
    filter_horizontal = ()


class CampsiteAdmin(admin.ModelAdmin):
    list_display = ('id', 'field_name', 'field_locality', 'field_address', 'field_postal_code', 'field_phone_number',
                    'field_email', 'field_website', 'ratings_number', 'average_rating', 'field_photo',
                    'field_description', 'field_owner')
    list_filter = ()
    ordering = ('id',)
    filter_horizontal = ()


class RatingAdmin(admin.ModelAdmin):
    list_display = ('id', 'value', 'comment', 'campsite', 'customer')
    list_filter = ()
    ordering = ('id',)
    filter_horizontal = ()


class ReservationAdmin(admin.ModelAdmin):
    list_display = ('id', 'arrival_date', 'departure_date', 'hour_of_reservation', 'status', 'customer', 'fieldOwner')
    list_filter = ()
    ordering = ('id',)
    filter_horizontal = ()


class PlaceTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'place_type', 'price', 'dimension', 'number_of_places', 'limit_of_places', 'campsite')
    list_filter = ()
    ordering = ('id',)
    filter_horizontal = ()


class PlaceAdmin(admin.ModelAdmin):
    list_display = ('id', 'placeType', 'reservation')
    list_filter = ()
    ordering = ('id',)
    filter_horizontal = ()


class ConvenienceAdmin(admin.ModelAdmin):
    list_display = ('id', 'canteen', 'wifi', 'shower', 'easy_access', 'parking', 'equipment_rental', 'campsite')
    list_filter = ()
    ordering = ('id',)
    filter_horizontal = ()


class StaticPageAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'contents')
    list_filter = ()
    ordering = ('id',)
    filter_horizontal = ()


admin.site.register(MyUser, UserAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(FieldOwner, FieldOwnerAdmin)
admin.site.register(Campsite, CampsiteAdmin)
admin.site.register(Rating, RatingAdmin)
admin.site.register(Reservation, ReservationAdmin)
admin.site.register(PlaceType, PlaceTypeAdmin)
admin.site.register(Place, PlaceAdmin)
admin.site.register(Convenience, ConvenienceAdmin)
admin.site.register(StaticPage, StaticPageAdmin)
admin.site.unregister(Group)
