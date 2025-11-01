package competition;

import competition.Team;

import java.util.HashMap;
import java.util.ArrayList;
import java.util.Collections;

public class Category {
  private final char LETTER;

  private int idealTimeM;
  private int allowedTimeM;
  private int maxTimeM;

  private int examExerciseN;
  private int liveCheckpointN;
  private int checkpointN;

  private static final float ALLOWED_TIME_RATIO = 1.5;
  private static final float MAX_TIME_RATIO = 1.75;
  private static final int ALLOWED_IDEAL_TIME_DEVIATION_M = 20;

  private static final Map<Character, Integer> RECOMMENDED_TIME_M;
  static {
    Map<Character, Integer> m = new HashMap<>();
    m.put('A', 120);
    m.put('B', 150);
    m.put('C', 180);
    m.put('D', 180);
    m.put('E', 150);
    m.put('F', 120);
    m.put('O', 150);
    RECOMMENDED_TIME_M = Collections.unmodifiableMap(m);
  }

  private final Map<String, Team> teams = new HashMap<>();

  public Category(char letter) { this.LETTER = letter; }

  // Competition
  public char getLetter() { return LETTER; }
  public boolean setIdealTimeM(int idealTimeM) {
    this.idealTimeM = idealTimeM;
    allowedTimeM = (int) Math.ceil(idealTimeM * ALLOWED_TIME_RATIO);
    maxTimeM = (int) Math.ceil(idealTimeM * MAX_TIME_RATIO);
    return Math.abs(RECOMMENDED_TIME_M.get(LETTER) - idealTimeM) <
      ALLOWED_IDEAL_TIME_DEVIATION_M;
  }
  public HashMap<Character, Integer> getRecommendedTimeM() {
    return RECOMMENDED_TIME_M;
  }
  public int getIdealTimeM() { return idealTimeM; }
  public int getAllowedTimeM() { return allowedTimeM; }
  public int getMaxTimeM() { return maxTimeM; }

  // Teams
  public boolean addTeam(Team team) {
    String name = team.getName;
    if (teams.containsKey(name) {
      return false;
    } else {
      teams.put(name, team);
      return true;
    }
  }
  public Team getTeam(String name) { return teams[name]; }

  // Checkpoints
  public boolean setExamExerciseN(int n) {
    examExerciseN = n;
    return true;
  }
  public int getExamExerciseN() { return examExerciseN; }
  public boolean setLiveCheckpointN(int n) {
    liveCheckpointN = n;
  }
  public int getLiveCheckpointN() { return liveCheckpointN; }
  public boolean setCheckpointN(int n) {
    checkpointN = n;
  }
  public int getCheckpointN() { return checkpointN; }
}

