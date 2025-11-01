package competition;

import competition.Category;

public class Team {
  private String name;
  private Category category;

  private int points = 0;
  private int correctExamExercises = 0;
  private int incorrectExamExercises = 0;
  private int correctDrawingExercises = 0;
  private int incorrectDrawingExercises = 0;
  private Boolean [] checkpointsFound = new Boolean[category.getCheckpointN()];

  public Team (String name, Category category) {
    this.name = name;
    this.category = category;
    category.addTeam(name, this);
  }

  // Competition
  public String getName() { return name; }
  public Category getCategory() { return category; }

  // Points
  public void addExamExercise(boolean correct) {
    if (correct) {
      correctExamExercises += 1;
    } else {
      incorrectExamExercises += 1;
    }
  }
  public int getPoints() { return points; }
  public int getCorrectExamExercises() { return correctExamExercises; }
}
