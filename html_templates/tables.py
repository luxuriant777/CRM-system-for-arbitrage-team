import django_tables2 as tables
from django.utils.html import format_html
from api_leads.models import Lead
from django_tables2 import A


class LeadTableByUser(tables.Table):
    id = tables.LinkColumn("html_templates:lead-detail", args=[A('id')], verbose_name="ID",
                           attrs={"a": {"style": "color: blue; text-decoration: underline;"}})
    ip_address = tables.Column(verbose_name="IP Address")
    user_agent = tables.Column(verbose_name="User Agent",
                               attrs={"td": {"style": "max-width: 300px; overflow: hidden; "
                                                      "text-overflow: ellipsis; white-space: nowrap;"}})
    referral_source = tables.Column(verbose_name="Referral Source")
    created_at = tables.Column(verbose_name="Created At")

    class Meta:
        model = Lead
        template_name = "django_tables2/bootstrap4.html"
        fields = ("id", "ip_address", "user_agent", "referral_source", "created_at")
        attrs = {"class": "table align-items-center mb-0 table-hover"}

    def render_user_agent(self, value):
        return format_html('<span title="{}">{}</span>', value, value)


class LeadTableAllUsers(LeadTableByUser):
    user_id = tables.LinkColumn("html_templates:user-detail", args=[A('user_id')], verbose_name="User ID",
                                attrs={"a": {"style": "color: blue; text-decoration: underline;"}})

    class Meta(LeadTableByUser.Meta):
        fields = LeadTableByUser.Meta.fields + ("user_id",)
        attrs = {"class": "table align-items-center mb-0 table-hover"}
