Feature: Support sessions.
  Group data points captured during a single session.

  Scenario: As a user I want to start a new session.
    Given a prepared subject wearing the EEG headset
    And system set up.
    When I start a measurement
    Then all data points captured will be accessible as one set.

  Scenario: As a user I want to start a new session with a given id.
    Given a prepared subject wearing the EEG headset
    And system set up.
    When starting measurements I enter a session id.
    Then all data points captured in this can be accessed using this session id.
