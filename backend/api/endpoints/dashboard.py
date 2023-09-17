from fastapi import APIRouter, Depends, Query
from crud import samples
from db import *
from models import *
from authentication import *
from pprint import pprint
from fastapi import APIRouter

router = APIRouter()


@router.get("/", response_model=DashboardGraph)
async def get_dashboard_data(
    selection_criterion: list = Query([]),
    current_user: User = Depends(get_current_active_user),
):
    """
    Retrieve dashboard data based on the provided selection criterion.

    Args:
        selection_criterion (list): A list of criteria to filter the samples.
        current_user (User): The current authenticated user.

    Returns:
        dict: A dictionary containing general statistics, dashboard data, and selection criterions.
    """
    graph_list = await samples.group_by_samples(selection_criterion)
    graph_list = fill_graph_data(graph_list)
    selection_criterions = await samples.get_selection_criterions()
    general_stats = await samples.get_general_stats()
    return {
        "general_stats": general_stats,
        "dashboard_data": graph_list,
        "selection_criterions": selection_criterions,
    }


def fill_graph_data(graph_list: list) -> list:
    """
    Fill the graph data with pangolins for each date. Used for plotting.

    Args:
        graph_list (list): A list of dictionaries containing date, pangolin, and pango_count.

    Returns:
        list: A sorted list of dictionaries with counts for pangolins.
    """
    dates = {}
    for graph in graph_list:
        if graph["date"] not in dates:
            dates[graph["date"]] = [graph["pangolin"]]
        else:
            dates[graph["date"]].append(graph["pangolin"])
    pangolins = [item for sublist in dates.values() for item in sublist]
    for date in dates:
        for pangolin in pangolins:
            if pangolin not in dates[date]:
                graph_list.append(
                    {"date": date, "pangolin": pangolin, "pango_count": 0}
                )
    graph_list = sorted(graph_list, key=lambda k: k["date"])
    return graph_list
