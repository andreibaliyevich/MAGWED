from django.contrib import admin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .models import MWUser, Customer, OrganizerRole, Organizer, UserLink


class DateJoinedFilter(admin.SimpleListFilter):
    title = _('Date joined')
    parameter_name = 'date_joined'
    
    def lookups(self, request, model_admin):
        return (
            ('last_3_days', _('Last 3 days')),
            ('last_week', _('Last week')),
            ('last_month', _('Last month')),
            ('last_6_months', _('Last 6 months')),
            ('last_year', _('Last year')),
            ('more_year', _('More year')),
        )
    
    def queryset(self, request, queryset):
        val = self.value()
        if val == 'last_3_days':
            date = timezone.now() - timezone.timedelta(days=3)
            return queryset.filter(date_joined__gte=date)
        elif val == 'last_week':
            date = timezone.now() - timezone.timedelta(weeks=1)
            return queryset.filter(date_joined__gte=date)
        elif val == 'last_month':
            date = timezone.now() - timezone.timedelta(days=30)
            return queryset.filter(date_joined__gte=date)
        elif val == 'last_6_months':
            date = timezone.now() - timezone.timedelta(days=180)
            return queryset.filter(date_joined__gte=date)
        elif val == 'last_year':
            date = timezone.now() - timezone.timedelta(days=365)
            return queryset.filter(date_joined__gte=date)
        elif val == 'more_year':
            date = timezone.now() - timezone.timedelta(days=365)
            return queryset.filter(date_joined__lt=date)


class UserLinkInline(admin.TabularInline):
    model = UserLink
    extra = 0


class MWUserAdmin(admin.ModelAdmin):
    """ User Model for admin """
    list_display = (
        'email',
        'name',
        'user_type',
        'is_active',
        'last_visit',
        'date_joined',
    )
    search_fields = ('email', 'name')
    list_filter = ('user_type', 'is_active', DateJoinedFilter)
    fieldsets = (
        (None, {
            'fields': ('user_type', 'email'),
        }),
        (_('Personal info'), {
            'fields': (
                'name',
                'avatar',
                'country',
                'city',
                'phone',
            ),
        }),
        (_('Permissions'), {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
            ),
        }),
        (_('Important dates'), {
            'fields': ('last_visit', 'last_login', 'date_joined'),
        }),
    )
    filter_horizontal = ('groups', 'user_permissions')
    readonly_fields = ('last_visit', 'last_login', 'date_joined')
    inlines = (UserLinkInline,)


class CustomerAdmin(admin.ModelAdmin):
    """ Customer Model for admin """
    list_display = ('user', 'date_of_wedding')


class OrganizerRoleAdmin(admin.ModelAdmin):
    """ Role of Organizer Model for admin """
    list_display = ('__str__',)


class OrganizerAdmin(admin.ModelAdmin):
    """ Organizer Model for admin """
    list_display = ('user', 'rating', 'pro_time')
    autocomplete_fields = ['countries', 'cities', 'languages']


admin.site.register(MWUser, MWUserAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(OrganizerRole, OrganizerRoleAdmin)
admin.site.register(Organizer, OrganizerAdmin)