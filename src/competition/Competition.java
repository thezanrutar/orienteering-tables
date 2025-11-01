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

  public void addCategory(Category category) {
    categories.add(category);
  }

  public void addTeam(Team team, String name) {
    if (allTeams.containsKey(name) {
      return false;
    } else {
      allTeams.put(name, team);
      return true;
    }
  }
}
