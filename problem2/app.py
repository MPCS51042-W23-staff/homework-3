import pathlib
from rich import print
from rich.prompt import Prompt, FloatPrompt
from rich.table import Table
from problem2 import SchoolSystem, Coordinate


def display_schools(title, schools, coord=None):
    """
    Display a list of schools in an easy to read table.

    Parameters:
        title: str                      Title of table for display.
        schools: list[School]           List of School objects.
        coord: Optional[Coordinate]     If provided, distance from coord will be shown.

    Returns: Nothing, prints output to screen.
    """
    table = Table(
        "ID", "Name", "Full Address", "Grades", "School Type", title=title
    )
    if coord:
        table.add_column("Distance", style="magenta")
    else:
        table.add_column("Location", style="magenta")

    for school in schools:
        table.add_row(
            # Dependency: public properties of School
            school.id,
            school.name,
            # Dependency: School.full_address
            school.full_address(),
            ", ".join(school.grades),
            school.school_type,
            # Dependency: Coord's string representation
            "{:.2f} miles".format(school.distance(coord)) if coord else str(school.location),
        )

    print(table)


def main():
    # Dependency: SchoolSystem constructor
    system = SchoolSystem(pathlib.Path(__file__).parent / "schools.csv")

    # Dependency: SchoolSystem.schools public member
    print(f"[green]School system loaded with {len(system.schools)} schools.")

    while True:

        which = Prompt.ask(
            "Search by [bold]\[l][/]ocation, [bold]\[g][/]rade, or [bold]\[t][/]ype? (Or E[bold]\[x][/]it.)",
            choices=["l", "g", "t", "x"],
        )

        if which == "x":
            exit()
        elif which == "l":
            lat = FloatPrompt.ask("Latitude")
            lng = FloatPrompt.ask("Longitude")
            distance = FloatPrompt.ask("Radius (miles)", default=1.0)
            coord = Coordinate(lat, lng)
            # Dependency: SchoolSystem.nearby_schools
            schools = system.nearby_schools(coord, distance)
            title = "Schools by Location"
        elif which == "g":
            grades = Prompt.ask("Enter grades, separated by commas")
            grades = [g.strip() for g in grades.split(",")]
            coord = None
            # Dependency: SchoolSystem.get_schools_by_grade
            schools = system.get_schools_by_grade(*grades)
            title = "Schools by Grade"
        elif which == "t":
            stype = Prompt.ask("Enter type of school")
            coord = None
            # Dependency: SchoolSystem.get_schools_by_type
            schools = system.get_schools_by_type(stype)
            title = "Schools by Type"

        display_schools(title, schools, coord)


if __name__ == "__main__":
    main()
