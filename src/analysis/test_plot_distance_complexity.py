from pathlib import Path

from src.analysis.plot_distance_complexity import make_figure


def test_make_figure_slope_and_files(tmp_path):
    out = tmp_path / "fig3-1_distance_complexity"
    slope = make_figure(Path("results/analysis/distance_complexity.csv"), out)
    assert 0.9 <= slope <= 1.3              # near-linear, not quadratic
    assert out.with_suffix(".png").exists()
    assert out.with_suffix(".pdf").exists()
