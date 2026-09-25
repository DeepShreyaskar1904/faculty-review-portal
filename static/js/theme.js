
/* =========================================================
   FACULTY REVIEW PORTAL
   GLOBAL THEME CONTROLLER
========================================================= */

(function () {

    "use strict";

    const STORAGE_KEY = "portal-theme";

    const root = document.documentElement;

    const toggle =
        document.getElementById("themeToggle");

    const icon =
        document.getElementById("themeIcon");

    const text =
        document.getElementById("themeText");

    const themeColorMeta =
        document.getElementById("themeColorMeta");


    function getTheme() {

        const current =
            root.getAttribute("data-theme");

        return current === "dark"
            ? "dark"
            : "light";
    }


    function updateThemeUI(theme) {

        if (!toggle) {
            return;
        }

        if (theme === "dark") {

            icon.className =
                "fa-solid fa-sun";

            text.textContent =
                "Light";

            toggle.setAttribute(
                "aria-label",
                "Switch to light mode"
            );

            toggle.setAttribute(
                "title",
                "Switch to light mode"
            );

            if (themeColorMeta) {
                themeColorMeta.setAttribute(
                    "content",
                    "#0f172a"
                );
            }

        } else {

            icon.className =
                "fa-solid fa-moon";

            text.textContent =
                "Dark";

            toggle.setAttribute(
                "aria-label",
                "Switch to dark mode"
            );

            toggle.setAttribute(
                "title",
                "Switch to dark mode"
            );

            if (themeColorMeta) {
                themeColorMeta.setAttribute(
                    "content",
                    "#f8fafc"
                );
            }
        }
    }


    function notifyThemeChange(theme) {

        window.dispatchEvent(
            new CustomEvent(
                "portal-theme-change",
                {
                    detail: {
                        theme: theme
                    }
                }
            )
        );
    }


    function applyTheme(theme) {

        const finalTheme =
            theme === "dark"
                ? "dark"
                : "light";

        root.setAttribute(
            "data-theme",
            finalTheme
        );

        localStorage.setItem(
            STORAGE_KEY,
            finalTheme
        );

        updateThemeUI(
            finalTheme
        );

        notifyThemeChange(
            finalTheme
        );

        updateChartTheme(
            finalTheme
        );
    }


    function updateChartTheme(theme) {

        if (
            typeof Chart === "undefined"
        ) {
            return;
        }

        const isDark =
            theme === "dark";

        const textColor =
            isDark
                ? "#e2e8f0"
                : "#475569";

        const gridColor =
            isDark
                ? "rgba(148,163,184,0.18)"
                : "rgba(100,116,139,0.15)";

        try {

            const instances =
                Chart.instances || {};

            Object.values(instances)
                .forEach(function (chart) {

                    if (!chart || !chart.options) {
                        return;
                    }

                    if (chart.options.plugins) {

                        if (
                            chart.options.plugins.legend
                        ) {
                            chart.options.plugins.legend.labels =
                                chart.options.plugins.legend.labels || {};

                            chart.options.plugins.legend.labels.color =
                                textColor;
                        }

                        if (
                            chart.options.plugins.tooltip
                        ) {
                            chart.options.plugins.tooltip.backgroundColor =
                                isDark
                                    ? "#0f172a"
                                    : "#ffffff";

                            chart.options.plugins.tooltip.titleColor =
                                isDark
                                    ? "#f8fafc"
                                    : "#172033";

                            chart.options.plugins.tooltip.bodyColor =
                                isDark
                                    ? "#e2e8f0"
                                    : "#334155";

                            chart.options.plugins.tooltip.borderColor =
                                isDark
                                    ? "#475569"
                                    : "#dbe3ef";

                            chart.options.plugins.tooltip.borderWidth =
                                1;
                        }
                    }


                    if (chart.options.scales) {

                        Object.values(
                            chart.options.scales
                        ).forEach(function (scale) {

                            if (scale.ticks) {
                                scale.ticks.color =
                                    textColor;
                            }

                            if (scale.grid) {
                                scale.grid.color =
                                    gridColor;
                            }

                            if (scale.title) {
                                scale.title.color =
                                    textColor;
                            }
                        });
                    }

                    chart.update();
                });

        } catch (error) {

            console.warn(
                "Theme chart update skipped:",
                error
            );
        }
    }


    /* Initial state */
    const savedTheme =
        localStorage.getItem(STORAGE_KEY);

    applyTheme(
        savedTheme === "dark"
            ? "dark"
            : "light"
    );


    /* Toggle */
    if (toggle) {

        toggle.addEventListener(
            "click",
            function () {

                const nextTheme =
                    getTheme() === "dark"
                        ? "light"
                        : "dark";

                applyTheme(
                    nextTheme
                );
            }
        );
    }


    /* Re-apply chart colors after Chart.js loads */
    window.addEventListener(
        "load",
        function () {

            setTimeout(
                function () {
                    updateChartTheme(
                        getTheme()
                    );
                },
                100
            );
        }
    );

})();
