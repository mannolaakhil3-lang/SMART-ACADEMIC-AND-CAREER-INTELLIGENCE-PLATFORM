/**
 * SMART ACADEMIC AND CAREER INTELLIGENCE PLATFORM (Team: G-2)
 * Client-side utilities and interactive helpers
 */

document.addEventListener("DOMContentLoaded", () => {
  // Pre-fill helper for the analysis form
  const fillDemoBtn = document.getElementById("fill-demo-btn");
  if (fillDemoBtn) {
    fillDemoBtn.addEventListener("click", () => {
      document.getElementById("name").value = "Demo Student";
      document.getElementById("branch").value = "CSE";
      document.getElementById("cgpa").value = "8.2";
      document.getElementById("skills").value = "Python, SQL, Problem Solving, Communication";
      document.getElementById("interests").value = "Technology, Data Science, Analytics";
      
      // Flash the fields briefly to show they have been populated
      const inputs = document.querySelectorAll(".form-control");
      inputs.forEach(input => {
        input.style.borderColor = "#2563eb";
        setTimeout(() => {
          input.style.borderColor = "";
        }, 600);
      });
    });
  }

  // Animate progress bars on results page
  const progressFills = document.querySelectorAll(".progress-bar-fill");
  progressFills.forEach(bar => {
    const targetWidth = bar.getAttribute("data-width") || "0%";
    bar.style.width = "0%";
    setTimeout(() => {
      bar.style.width = targetWidth;
    }, 150);
  });
});
