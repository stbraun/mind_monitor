Feature: Support sessions.
  Group data points captured during a single session.

  Scenario: As a user I want to start a new session.
    Given system is set up.
    When I start a session
    Then all data points captured will be accessible as one set.

  Scenario: As a user I want to start a new session with a given id.
    Given system is set up.
    When starting measurements I enter a session id.
    Then all data points captured in this can be accessed using this session id.
