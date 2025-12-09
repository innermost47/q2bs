import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime as dt, timedelta


class Q2BDataVisualizer:
    def __init__(self, input_dir):
        self.input_dir = input_dir

    def create_visualizations(self, report):
        print("\nCreating visualizations...")

        graphs_dir = os.path.join(self.input_dir, "graphs")
        os.makedirs(graphs_dir, exist_ok=True)

        plt.style.use("seaborn-v0_8-darkgrid")
        colors = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#FFA07A", "#98D8C8"]

        self.plot_daily_articles(report, graphs_dir, colors)
        self.plot_daily_timeline(report, graphs_dir, colors)
        self.plot_stats_summary(report, graphs_dir, colors)

        print(f"Graphs saved in: {graphs_dir}")

    def plot_daily_articles(self, report, output_dir, colors):
        daily_data = report["daily_statistics"]["articles_per_day"]

        if not daily_data:
            return

        _, ax = plt.subplots(figsize=(14, 8))

        dates = list(daily_data.keys())
        counts = list(daily_data.values())

        earliest = report["date_range"]["earliest"]
        latest = report["date_range"]["latest"]

        bar_colors = []
        for date in dates:
            if date == earliest or date == latest:
                bar_colors.append("#CCCCCC")
            elif date == max(daily_data, key=daily_data.get):
                bar_colors.append(colors[1])
            else:
                bar_colors.append(colors[0])

        ax.bar(
            dates, counts, color=bar_colors, alpha=0.8, edgecolor="black", linewidth=1.5
        )

        num_days = len(dates)

        important_indices = set()

        peak_date = max(daily_data, key=daily_data.get)
        if peak_date in dates:
            important_indices.add(dates.index(peak_date))

        important_indices.add(0)
        important_indices.add(len(dates) - 1)

        if num_days <= 15:
            indices_to_show = set(range(num_days))
            font_size = 10
        elif num_days <= 30:
            indices_to_show = set(range(0, num_days, 2)) | important_indices
            font_size = 9
        elif num_days <= 90:
            indices_to_show = set(range(0, num_days, 5)) | important_indices
            font_size = 8
        elif num_days <= 180:
            indices_to_show = set(range(0, num_days, 10)) | important_indices
            font_size = 8
        else:
            indices_to_show = important_indices
            font_size = 9

        for i, (date, count) in enumerate(zip(dates, counts)):
            if i in indices_to_show:
                label = f"{count:,}"
                if date == earliest or date == latest:
                    label += "\n(partial)"

                if num_days > 180 and i in important_indices:
                    label = f"{date}\n{label}"

                ax.text(
                    i,
                    count + max(counts) * 0.02,
                    label,
                    ha="center",
                    va="bottom",
                    fontsize=font_size,
                    fontweight="bold",
                )

        avg = report["daily_statistics"]["average_per_day"]
        ax.axhline(
            y=avg,
            color="red",
            linestyle="--",
            linewidth=2,
            label=f"Average: {avg:,.0f} articles/day (excl. partial days)",
            alpha=0.7,
        )

        ax.set_xlabel("Date", fontsize=14, fontweight="bold")
        ax.set_ylabel("Number of Articles", fontsize=14, fontweight="bold")

        date_range = f"{earliest} to {latest}"
        label_info = (
            f"\nShowing {len(indices_to_show)} of {num_days} days"
            if num_days > 90
            else ""
        )
        ax.set_title(
            f'Q2BSTUDIO: Daily Article Production\n"Industrial-Scale Automated Content Generation"\nData Period: {date_range}{label_info}\nNote: First and last days excluded from average (incomplete data)',
            fontsize=14,
            fontweight="bold",
            pad=20,
        )

        ax.legend(fontsize=12, loc="upper left")
        ax.grid(True, alpha=0.3, axis="y")

        if num_days <= 7:
            plt.xticks(rotation=0)
        elif num_days <= 31:
            plt.xticks(rotation=45, ha="right")
        elif num_days <= 90:
            tick_positions = list(range(0, num_days, 7))
            tick_labels = [dates[i] if i < len(dates) else "" for i in tick_positions]
            plt.xticks(tick_positions, tick_labels, rotation=45, ha="right")
        elif num_days <= 365:
            tick_positions = list(range(0, num_days, 30))
            tick_labels = [dates[i] if i < len(dates) else "" for i in tick_positions]
            plt.xticks(tick_positions, tick_labels, rotation=45, ha="right")
        elif num_days <= 730:
            tick_positions = list(range(0, num_days, 60))
            tick_labels = [dates[i] if i < len(dates) else "" for i in tick_positions]
            plt.xticks(tick_positions, tick_labels, rotation=45, ha="right")
        else:
            tick_positions = list(range(0, num_days, 180))
            tick_labels = [dates[i] if i < len(dates) else "" for i in tick_positions]
            plt.xticks(tick_positions, tick_labels, rotation=45, ha="right")

        plt.tight_layout()
        plt.savefig(
            os.path.join(output_dir, "1_daily_articles.png"),
            dpi=300,
            bbox_inches="tight",
        )
        plt.close()

        print("Created: 1_daily_articles.png")

    def plot_daily_timeline(self, report, output_dir, colors):
        daily_data = report["daily_statistics"]["articles_per_day"]

        if not daily_data:
            return

        _, ax = plt.subplots(figsize=(14, 8))

        dates_str = list(daily_data.keys())

        valid_dates_str = [d for d in dates_str if d != "UNKNOWN_DATE"]
        if not valid_dates_str:
            print(
                "No valid dates after filtering 'UNKNOWN_DATE'. Skipping 2_timeline.png"
            )
            return

        valid_dates_str.sort()

        dates = [dt.strptime(d, "%Y-%m-%d") for d in valid_dates_str]
        counts = [daily_data[d_str] for d_str in valid_dates_str]

        earliest = report["date_range"]["earliest"]
        latest = report["date_range"]["latest"]

        ax.plot(
            dates,
            counts,
            marker="o",
            markersize=12,
            linewidth=3,
            color=colors[3],
            label="Articles Published",
            markeredgecolor="black",
            markeredgewidth=2,
        )

        ax.fill_between(dates, counts, alpha=0.3, color=colors[3])

        dates_calc = [d for d in valid_dates_str if d != earliest and d != latest]
        if dates_calc:
            peak_date_str = max(dates_calc, key=lambda d: daily_data[d])
            max_idx = valid_dates_str.index(peak_date_str)

            ax.plot(
                dates[max_idx],
                counts[max_idx],
                marker="*",
                markersize=25,
                color="red",
                label=f"Peak: {counts[max_idx]:,} articles ({peak_date_str})",
                markeredgecolor="black",
                markeredgewidth=2,
            )

        num_days = (dates[-1] - dates[0]).days if dates else 0

        if num_days > 365 * 2:
            ax.xaxis.set_major_locator(mdates.YearLocator())
            ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
        elif num_days > 90:
            ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
            ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
        elif num_days > 30:
            ax.xaxis.set_major_locator(
                mdates.WeekdayLocator(byweekday=mdates.MO, interval=2)
            )
            ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
        else:
            ax.xaxis.set_major_locator(mdates.DayLocator())
            ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))

        ax.set_xlabel("Date", fontsize=14, fontweight="bold")
        ax.set_ylabel("Articles Published", fontsize=14, fontweight="bold")

        avg = report["daily_statistics"]["average_per_day"]
        avg_seconds = 86400 / avg if avg > 0 else 0

        date_range = f"{earliest} to {latest}"
        ax.set_title(
            f"Publication Timeline: {date_range}\nAverage: 1 article every {avg_seconds:.1f} seconds",
            fontsize=14,
            fontweight="bold",
            pad=20,
        )

        ax.legend(fontsize=12, loc="best")
        ax.grid(True, alpha=0.3)

        if num_days > 30 or len(dates) > 10:
            plt.xticks(rotation=45, ha="right")
        else:
            plt.xticks(rotation=0)

        plt.tight_layout()
        plt.savefig(
            os.path.join(output_dir, "2_timeline.png"), dpi=300, bbox_inches="tight"
        )
        plt.close()

        print("Created: 2_timeline.png")

    def plot_stats_summary(self, report, output_dir, colors):

        daily_data = report["daily_statistics"]["articles_per_day"]
        valid_data = {k: v for k, v in daily_data.items() if k != "UNKNOWN_DATE"}

        last_4_weeks_data = {}
        last_4_weeks_total = 0
        last_4_weeks_peak = 0

        if valid_data:
            try:
                latest_date_str = max(valid_data.keys())
                latest_date = dt.strptime(latest_date_str, "%Y-%m-%d")
                four_weeks_ago = latest_date - timedelta(days=28)

                for date_str, count in valid_data.items():
                    date_obj = dt.strptime(date_str, "%Y-%m-%d")
                    if date_obj >= four_weeks_ago:
                        last_4_weeks_data[date_str] = count
                        last_4_weeks_total += count
                        if count > last_4_weeks_peak:
                            last_4_weeks_peak = count
            except:
                last_4_weeks_data = valid_data
                last_4_weeks_total = sum(valid_data.values())
                last_4_weeks_peak = max(valid_data.values()) if valid_data else 0

        num_days = len(last_4_weeks_data)
        last_4_weeks_avg = last_4_weeks_total / num_days if num_days > 0 else 0

        if last_4_weeks_data:
            earliest_4w = min(last_4_weeks_data.keys())
            latest_4w = max(last_4_weeks_data.keys())
            date_range_4w = f"{earliest_4w} to {latest_4w}"
        else:
            date_range_4w = "No data"

        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))

        fig.suptitle(
            f"Q2BSTUDIO Content Farm: Statistical Analysis (Last 4 Weeks)\nPeriod: {date_range_4w}",
            fontsize=18,
            fontweight="bold",
            y=0.98,
        )

        ax1.text(
            0.5,
            0.6,
            f"{last_4_weeks_total:,}",
            ha="center",
            va="center",
            fontsize=60,
            fontweight="bold",
            color=colors[0],
        )
        ax1.text(
            0.5,
            0.35,
            "Articles Published\n(Last 4 Weeks)",
            ha="center",
            va="center",
            fontsize=18,
            fontweight="bold",
        )
        ax1.axis("off")
        ax1.set_facecolor("#f0f0f0")

        ax2.text(
            0.5,
            0.6,
            f"{last_4_weeks_avg:,.0f}",
            ha="center",
            va="center",
            fontsize=60,
            fontweight="bold",
            color=colors[1],
        )
        ax2.text(
            0.5,
            0.35,
            "Articles Per Day\n(Last 4 Weeks Avg)",
            ha="center",
            va="center",
            fontsize=18,
            fontweight="bold",
        )
        seconds = 86400 / last_4_weeks_avg if last_4_weeks_avg > 0 else 0
        ax2.text(
            0.5,
            0.15,
            f"1 article every {seconds:.1f} seconds",
            ha="center",
            va="center",
            fontsize=25,
            color="red",
            fontweight="bold",
        )
        ax2.axis("off")
        ax2.set_facecolor("#f0f0f0")

        ax3.text(
            0.5,
            0.6,
            f"{last_4_weeks_peak:,}",
            ha="center",
            va="center",
            fontsize=60,
            fontweight="bold",
            color=colors[2],
        )
        ax3.text(
            0.5,
            0.35,
            "Peak Day\n(Last 4 Weeks Max)",
            ha="center",
            va="center",
            fontsize=18,
            fontweight="bold",
        )
        peak_seconds = 86400 / last_4_weeks_peak if last_4_weeks_peak > 0 else 0
        ax3.text(
            0.5,
            0.15,
            f"1 article every {peak_seconds:.1f} seconds",
            ha="center",
            va="center",
            fontsize=25,
            fontweight="bold",
            color="red",
        )
        ax3.axis("off")
        ax3.set_facecolor("#f0f0f0")

        comparisons = [
            ("TechCrunch", 40),
            ("The Verge", 30),
            ("NY Times", 250),
            ("Q2BSTUDIO\n(Last 4 Weeks)", last_4_weeks_avg),
        ]

        names = [c[0] for c in comparisons]
        values = [c[1] for c in comparisons]

        bars = ax4.barh(
            names,
            values,
            color=[colors[4], colors[4], colors[4], colors[0]],
            edgecolor="black",
            linewidth=1.5,
        )

        bars[-1].set_alpha(1.0)

        for i, (_, value) in enumerate(zip(names, values)):
            ax4.text(
                value + max(values) * 0.02,
                i,
                f"{value:,.0f}",
                va="center",
                fontsize=12,
                fontweight="bold",
            )

        ax4.set_xlabel("Articles Per Day", fontsize=12, fontweight="bold")
        ax4.set_title(
            "Comparison: Daily Output (Last 4 Weeks)\n(Industry estimates - conservative)",
            fontsize=14,
            fontweight="bold",
            pad=10,
        )
        ax4.grid(True, alpha=0.3, axis="x")

        plt.tight_layout()
        plt.savefig(
            os.path.join(output_dir, "3_stats_summary.png"),
            dpi=300,
            bbox_inches="tight",
        )
        plt.close()

        print("Created: 3_stats_summary.png")
