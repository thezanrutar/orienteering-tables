package competition;

import competition.Category;
import competition.Team;

import java.util.HashSet;

public class Competition {
  private String title;
  private Set<Category> categories = new HashSet<>();
  private Map<String, Team> allTeams = new HashMap<>();

  public Competition(String title) {
    this.title = title;
  }

  public addCategory(Category category) {
    categories.add(category);
  }

  public addTeam(Team team, String name) {
    allTeams.add(name, team);
  }
}
