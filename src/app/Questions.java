package app;

import competition.Team;

public static class Questions {
  private final char LETTER;

  private String [] questionsA = {
    "Team category:",
    "Team name:",
    "Team club:",
    "Members:",


  public Questions(Category category) {
    LETTER = category.getLetter();
  }

}
