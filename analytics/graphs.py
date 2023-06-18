from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import datetime
from django.db.models import Count
from django.db.models.functions import TruncDay, TruncHour
from django_plotly_dash import DjangoDash
from api_users.models import CustomUser, Position
from api_prospects.models import Prospect
from api_teams.models import Team


team_lead_app = DjangoDash("TeamLeadApp")
buyer_app = DjangoDash("BuyerApp")
prospect_app = DjangoDash("ProspectApp")
team_app = DjangoDash("TeamApp")

def fetch_data(obj, attribute, position=None):
    data = obj.annotate(attribute=attribute("created_at"))
    if position is not None:
        data = data.filter(position=position)
    data = data.values("attribute").annotate(c=Count("id")).values("attribute", "c")
    df = pd.DataFrame.from_records(data)
    return df

def generate_figure(df, color, title, hover_template):
    x = df.columns[0]
    return {
        "data": [
            go.Scatter(
                x=df[x],
                y=df["c"],
                mode="lines",
                name=title,
                line=dict(color=color),
                fill="tozeroy",
                fillcolor=color.replace(", 1)", ", 0.2)"),
                line_shape="spline",
                hovertemplate=hover_template
            )
        ],
        "layout": go.Layout(
            title=title,
            xaxis=dict(title="Timeline"),
            yaxis=dict(title="Number of " + title),
            showlegend=False
        )
    }

def generate_bar_chart(team_members_df):
    return {
        "data": [
            go.Bar(
                x=team_members_df["name"],
                y=team_members_df["c"],
                name="Team Members",
                marker=dict(color="rgba(255, 99, 132, 0.2)")
            )
        ],
        "layout": go.Layout(
            title="Team Members",
            xaxis=dict(title="Team"),
            yaxis=dict(title="# of Team Members"),
            showlegend=False
        )
    }

def generate_bar_chart_v2(df, x_col, y_col, title):
    return {
        "data": [
            go.Bar(
                x=df[x_col],
                y=df[y_col],
                name=title,
                marker=dict(color="rgba(255, 99, 132, 0.2)")
            )
        ],
        "layout": go.Layout(
            title=title,
            xaxis=dict(title="Team"),
            yaxis=dict(title=title),
            showlegend=False
        )
    }

def get_prospects_generated_by_each_team():
    prospects_df = pd.DataFrame(list(Prospect.objects.values()))
    users_df = pd.DataFrame(list(CustomUser.objects.values()))
    prospects_users_df = pd.merge(prospects_df, users_df, left_on="user_id", right_on="id", suffixes=("_prospect", "_user"))
    teams_df = pd.DataFrame(list(Team.objects.values("id", "name")))
    team_members_df = pd.DataFrame(list(Team.members.through.objects.values("customuser_id", "team_id")))
    prospects_teams_rel_df = pd.merge(prospects_users_df, team_members_df, left_on="id_user", right_on="customuser_id")
    prospects_teams_name_df = pd.merge(prospects_teams_rel_df, teams_df, left_on="team_id", right_on="id")
    team_prospects_count = prospects_teams_name_df.groupby("name")["id_prospect"].count().reset_index().rename(
        columns={"id_prospect": "prospects_count", "name": "team_name"})
    return team_prospects_count

def get_team_members():
    team_members_qs = Team.objects.annotate(c=Count("members")).values("name", "c")
    return pd.DataFrame.from_records(team_members_qs)

def create_graphs():
    today = datetime.datetime.now()
    start_of_week = today - datetime.timedelta(days=today.weekday())
    end_of_week = start_of_week + datetime.timedelta(days=6)

    date_picker = dcc.DatePickerRange(
        id="date-picker-range",
        start_date=start_of_week.date(),
        end_date=end_of_week.date(),
    )

    team_lead_graph = dcc.Graph(id="team-lead-graph")
    buyer_graph = dcc.Graph(id="buyer-graph")
    prospect_graph = dcc.Graph(id="prospect-graph")
    team_chart = dcc.Graph(id="team-chart")

    dropdown = html.Div(
        dcc.Dropdown(
            id="team-dropdown",
            options=[
                {"label": "Members Count", "value": "mc"},
                {"label": "Prospects Count", "value": "pc"}
            ],
            value="mc",
            style={"width": "230px", "fontSize": "25px"}
        ),
        style={"display": "flex", "alignItems": "center"}
    )

    return date_picker, team_lead_graph, buyer_graph, prospect_graph, dropdown, team_chart

date_picker, team_lead_graph, buyer_graph, prospect_graph, dropdown, team_chart = create_graphs()

team_lead_app.layout = html.Div(children=[date_picker, team_lead_graph])
buyer_app.layout = html.Div(children=[date_picker, buyer_graph])
prospect_app.layout = html.Div(children=[date_picker, prospect_graph])
team_app.layout = html.Div([
    html.Div([dropdown], style={"marginBottom": "14px"}),
    html.Div([team_chart])
])

def create_graph_callback(output_id, model, obj, position, color, title, hovertemplate):
    @model.callback(
        Output(output_id, "figure"),
        [Input("date-picker-range", "start_date"), Input("date-picker-range", "end_date")]
    )
    def update_graph_output(start_date, end_date):
        start_date_obj = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        end_date_obj = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        date_diff = (end_date_obj - start_date_obj).days

        attribute = TruncHour if date_diff <= 7 else TruncDay
        df = fetch_data(obj, attribute, position)
        df = df[(df[df.columns[0]] > start_date) & (df[df.columns[0]] < end_date)]
        return generate_figure(df, color, title, hovertemplate + "<extra></extra>")

create_graph_callback("team-lead-graph", team_lead_app, CustomUser.objects, Position.TEAM_LEAD,
                      "rgba(0, 123, 255, 1)", "Team Leads", "Date: %{x}<br>Number of Team Leads: %{y}")
create_graph_callback("buyer-graph", buyer_app, CustomUser.objects, Position.BUYER,
                      "rgba(40, 167, 69, 1)", "Buyers", "Date: %{x}<br>Number of Buyers: %{y}")
create_graph_callback("prospect-graph", prospect_app, Prospect.objects, None,
                      "rgba(153, 102, 255, 1)", "Prospects", "Date: %{x}<br>Number of Prospects: %{y}")

@team_app.callback(
    Output("team-chart", "figure"),
    [Input("team-dropdown", "value")]
)
def update_team_chart(value):
    if value == "mc":
        team_members_df = get_team_members()
        return generate_bar_chart_v2(team_members_df, "name", "c", "Number of Team Members")
    elif value == "pc":
        team_prospects_df = get_prospects_generated_by_each_team()
        return generate_bar_chart_v2(team_prospects_df, "team_name", "prospects_count", "Number of Prospects generated by each Team")
