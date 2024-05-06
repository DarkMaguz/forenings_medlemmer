import codecs
from django.contrib import admin
from django.db.models import Q
from django.http import HttpResponse
from django.utils.html import format_html

from members.models import (
    Department,
    Person,
)

from .person_admin_filters import (
    PersonInvitedListFilter,
    PersonParticipantActiveListFilter,
    PersonParticipantCurrentYearListFilter,
    PersonParticipantLastYearListFilter,
    PersonParticipantListFilter,
    PersonWaitinglistListFilter,
    VolunteerListFilter,
)

from .inlines import (
    ActivityInviteInline,
    PaymentInline,
    VolunteerInline,
    WaitingListInline,
)

from members.admin.admin_actions import AdminActions


class PersonAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "membertype",
        "gender_text",
        "family_url",
        "age_years",
        "zipcode",
        "added_at",
        "notes",
    )
    list_filter = (
        "membertype",
        "gender",
        VolunteerListFilter,
        PersonWaitinglistListFilter,
        PersonInvitedListFilter,
        PersonParticipantListFilter,
        PersonParticipantActiveListFilter,
        PersonParticipantCurrentYearListFilter,
        PersonParticipantLastYearListFilter,
    )
    search_fields = ("name", "family__email", "notes")
    actions = [
        AdminActions.invite_many_to_activity_action,
        "export_emaillist",
        "export_csv",
    ]
    raw_id_fields = ("family", "user")

    inlines = [
        PaymentInline,
        VolunteerInline,
        ActivityInviteInline,
        WaitingListInline,
    ]

    def family_url(self, item):
        return format_html(
            '<a href="../family/%d">%s</a>' % (item.family.id, item.family.email)
        )

    family_url.allow_tags = True
    family_url.short_description = "Familie"
    list_per_page = 20

    def gender_text(self, item):
        return item.gender_text()

    gender_text.short_description = "Køn"

    # needs 'view_full_address' to set personal details.
    # email and phonenumber only shown on adults.
    def get_fieldsets(self, request, person=None):
        if request.user.has_perm("members.view_full_address"):
            contact_fields = (
                "name",
                "streetname",
                "housenumber",
                "floor",
                "door",
                "city",
                "zipcode",
                "placename",
                "email",
                "phone",
                "family",
            )
        else:
            if person.membertype == Person.CHILD:
                contact_fields = ("name", "city", "zipcode", "family")
            else:
                contact_fields = ("name", "city", "zipcode", "email", "phone", "family")

        fieldsets = (
            ("Kontakt Oplysninger", {"fields": contact_fields}),
            ("Noter", {"fields": ("notes",)}),
            (
                "Yderlige informationer",
                {
                    "classes": ("collapse",),
                    "fields": (
                        "membertype",
                        "birthday",
                        "has_certificate",
                        "added_at",
                        "user",
                        "gender",
                    ),
                },
            ),
        )

        return fieldsets

    def get_readonly_fields(self, request, obj=None):
        if type(obj) == Person and not request.user.is_superuser:
            return [
                "name",
                "streetname",
                "housenumber",
                "floor",
                "door",
                "city",
                "zipcode",
                "placename",
                "email",
                "phone",
                "family",
                "membertype",
                "birthday",
                "has_certificate",
                "added_at",
            ]
        else:
            return []

    def unique(self, item):
        return item.family.unique if item.family is not None else ""

    def export_emaillist(self, request, queryset):
        result_string = "kopier denne liste direkte ind i dit email program (Husk at bruge Bcc!)\n\n"
        family_email = []
        for person in queryset:
            if not person.family.dont_send_mails:
                family_email.append(person.family.email)
        result_string = result_string + ";\n".join(list(set(family_email)))
        result_string = (
            result_string
            + "\n\n\nHusk nu at bruge Bcc! ... IKKE TO: og heller IKKE CC: felterne\n\n"
        )

        return HttpResponse(result_string, content_type="text/plain")

    export_emaillist.short_description = "Exporter e-mail liste"

    def export_csv(self, request, queryset):
        result_string = "Navn;Alder;Opskrevet;Tlf (barn);Email (barn);"
        result_string += "Tlf (forælder);Email (familie);Postnummer;Noter\n"
        for person in queryset:
            parent = person.family.get_first_parent()
            if parent:
                parent_phone = parent.phone
            else:
                parent_phone = ""

            if not person.family.dont_send_mails:
                person_email = person.email
                family_email = person.family.email
            else:
                person_email = ""
                family_email = ""

            result_string = (
                result_string
                + person.name
                + ";"
                + str(person.age_years())
                + ";"
                + str(person.added_at.strftime("%Y-%m-%d %H:%M"))
                + ";"
                + person.phone
                + ";"
                + person_email
                + ";"
                + parent_phone
                + ";"
                + family_email
                + ";"
                + person.zipcode
                + ";"
                + '"'
                + person.notes.replace('"', '""')
                + '"'
                + "\n"
            )
            response = HttpResponse(
                f'{codecs.BOM_UTF8.decode("utf-8")}{result_string}',
                content_type="text/csv; charset=utf-8",
            )
            response["Content-Disposition"] = 'attachment; filename="personer.csv"'
        return response

    export_csv.short_description = "CSV Export"

    # Only view persons related to users department (all family, via participant, waitinglist & invites)
    def get_queryset(self, request):
        qs = super(PersonAdmin, self).get_queryset(request)
        if (
            request.user.is_superuser
            or request.user.has_perm("members.view_all_persons")
            or request.user.has_perm("members.view_all_departments")
        ):
            return qs
        else:
            departments = Department.objects.filter(
                adminuserinformation__user=request.user
            ).values("id")
            return qs.filter(
                Q(
                    family__person__activityparticipant__activity__department__in=departments
                )
                | Q(family__person__waitinglist__department__in=departments)
                | Q(
                    family__person__activityinvite__activity__department__in=departments
                )
            ).distinct()
