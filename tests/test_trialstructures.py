import DataProcessingTools as DPT
import numpy as np
import os

def test_basic():
    events = [("trial_start", 0.1),
              ("target_on", 0.2),
              ("target_off", 0.5),
              ("reward_on", 0.6),
              ("reward_off", 0.8),
              ("trial_end", 0.85),
              ("trial_start", 1.1),
              ("target_on", 1.2),
              ("target_off", 1.5),
              ("failure_on", 1.6),
              ("failure_off", 1.8),
              ("trial_end", 1.85)]

    trials = DPT.trialstructures.TrialStructure()
    trials.events = np.array([event[0] for event in events])
    trials.timestamps = np.array([event[1] for event in events])

    trial_starts = trials.get_timestamps("trial_start")
    assert (trial_starts == [0.1, 1.1]).all()

def test_working_memory():
    testdir = "animal/20130923"
    with DPT.misc.CWD(os.path.join(os.path.dirname(__file__),testdir)):
        trials = DPT.trialstructures.WorkingMemoryTrials()
        assert len(trials.events) == 12746
        trial_starts = trials.get_timestamps("trial_start")
        assert len(trial_starts) == 1733
        assert np.allclose(trial_starts[:2], [47.7139, 50.11616667])

        stim1_onset = trials.get_timestamps("stimulus_on_1_*")
        assert len(stim1_onset) == 1915
        assert np.allclose(stim1_onset[-5:], 
                            [9107.5137, 9117.90566667, 9164.79406667, 9254.83466667, 9259.95556667])

        stim1_offset = trials.get_timestamps("stimulus_off_1_*")
        assert len(stim1_offset) == len(stim1_onset)
        reward_on = trials.get_timestamps("reward_on")
        assert len(reward_on) == 395

def test_auto_discovery():
    testdir = "animal/20130923/session01/array01/channel001/cell01"
    with DPT.misc.CWD(os.path.join(os.path.dirname(__file__), testdir)):
        trials = DPT.trialstructures.get_trials()
        assert len(trials.events) == 12746