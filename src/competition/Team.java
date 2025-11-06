package competition;

import java.util.*;

public class Team {
  private String name;
  private Category category;

  private int points;
  private int startPoints;
  private int [] examValues = new Integer[2];
  private int [] drawingValues = new Integer[2];
  private int [] livePoints =
    new Integer[category.getLiveCheckpointN];
  private int checkpointsFound;

  private int membersN;
  private int women;
  private int children;
  private int elderly;

  private boolean firstAid;
  private boolean shoes;
  private boolean membership;

  private String [] members;
  private String club;
  private String contact;

  public Team (String name, Category category) {
    this.name = name;
    this.category = category;
    category.addTeam(name, this);
  }

  // Competition
  public String getName() { return name; }
  public Category getCategory() { return category; }

  // Team
  public void addMembersN(int n) {
    membersN = n;
    members = new String[membersN];
  }

  // Points
  private void calculatePoints() {
    int examPoints = examValues[0] * 5 - examValues[1] * 2;
    int drawingPoints = drawingValues[0] * 20 - drawingValues[1] * 5;
    int liveCheckpointPoints;
    for (int x : livePoints) {
      livePoints += x;
    }
    int checkpointPoints = checkpointsFound * 50;
    points = startPoints + (
      examPoints + drawingPoints + liveChecpointPoints + checkpointPoints
    );
  }
  public void setCheckpoints(int n) {
    checkpointsFound = n;
    calculatePoints();
  }
  public void addExamValues(int correct, int incorrect) {
    examValues[0] += correct;
    examValues[1] += incorrect;
    calculatePoints();
  }
  public void addDrawingValues(int correct, int incorrect) {
    drawingValues[0] += correct;
    drawingValues[1] += incorrect;
  }
  public void addLivePoints(int i, int points) {
    livePoints[i] = points;
    calculatePoints();
  }
  public int getPoints() { return points; }
}
