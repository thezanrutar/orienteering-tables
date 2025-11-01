package competition;

import competition.Category;

public class Team {
  private String name;
  private Category category;

  public Team (String name, Category category) {
    this.name = name;
    this.category = category;
    category.addTeam(name, this);
  }

  public String getName() { return name; }
  public Category getCategory() { return category; }
}
