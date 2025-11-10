package competition;

import java.util.*;

public class Team {
  private String name;
  private Category category;

  private int points;
  private int startPoints;
  private int [] examValues = new Integer[2];
  private int [] drawingValues = new Integer[2];
  private int [] livePoints;
  private int checkpointsFound;

  private int membersN;
  private int womenN;
  private int childrenN;
  private int elderlyN;

  private boolean firstAid = true;
  private int shoesN; // more negative => worse
  private boolean membership;

  private String [] members;
  private String club;
  private String contact;

  public Team (String name, Category category) {
    this.name = name;
    this.category = category;
    category.addTeam(name, this);
    livePoints = new Integer[category.getLiveCheckpointN];
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
  private void calculateStartPoints() {
    int firstAidPoints = firstAid ? 0 : -15;
    int membershipPoints = membership ? 0 : -10;
    int shoesPoints;
    if (shoesN >= 3) {
      shoesPoints = -15;
    } else if (shoesN == 2) {
      shoesPoints = -10;
    } else if (shoesN == 1) {
      shoesPoints = -5;
    } else { shoesPoints = 0; }
    int womenPoints = womenN * 2;
    int elderlyPoints = elderlyN * 2;
    int childrenPoints;
    if (childrenN >= 2) {
      childrenPoints = 10;
    } else if (childrenN == 1) {
      childrenPoints = 5;
    } else { childrenPoints = 0; }
    int memberPoints;
    switch (membersN) {
      case 5:
        memberPoints = 10;
        break;
      case 2:
        memberPoints = -10;
        break;
      default:
        memberPoints = 0;
    }
    startPoints = firstAidPoints + memberPoints + shoesPoints
      + womenPoints + elderlyPoints + childrenPoints + memberPoints;
  }
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
    calculatePoints();
  }
  public void addLivePoints(int i, int points) {
    livePoints[i] = points;
    calculatePoints();
  }
  public int getPoints() { return points; }
}
