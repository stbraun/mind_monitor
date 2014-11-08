Feature: Capture pre-processed EEG data.
  Beneath the raw data pre-processed data like alpha, delta, and other waves.

  Scenario: As a user I want to capture wave records.
    Given system is set up.
    When I select pre-processed data
    And I start a measurement
    Then pre-processed data is captured.
