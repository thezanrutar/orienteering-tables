package competition;

import java.util.HashSet;

public class Competition {
  private String title;
  private HashSet<Category> categories = new HashSet<Category>;

  public Competition(String title) {
    this.title = title;
  }

  public addCategory(Category category) {
    categories.add(category);
  }
}
