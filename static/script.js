/**
 * SMART ACADEMIC AND CAREER INTELLIGENCE PLATFORM (Team: G-2)
 * Client-side Controller & Dynamic Features
 * - Form pre-fill and reset helpers
 * - Real-time processing simulation overlay
 * - LocalStorage learning plan step persistence
 * - Interactive Career Details modal
 * - Print report handlers
 */

document.addEventListener("DOMContentLoaded", () => {

  // =========================================================================
  // 1. ANALYSIS FORM LOGIC (Pre-fill, Reset, Processing Overlay)
  // =========================================================================
  const careerForm = document.getElementById("career-form");
  const fillDemoBtn = document.getElementById("fill-demo-btn");
  const resetFormBtn = document.getElementById("reset-form-btn");
  const loadingOverlay = document.getElementById("loading-overlay");

  if (fillDemoBtn) {
    fillDemoBtn.addEventListener("click", () => {
      const fieldValues = {
        name: "Demo Student",
        branch: "CSE",
        academic_year: "3rd Year",
        cgpa: "8.2",
        skills: "Python, SQL, Problem Solving, Communication",
        interests: "Technology, Data Science, Analytics",
        soft_skills: "Teamwork, Analytical Thinking, Communication",
        career_preference: "Data Analyst"
      };

      Object.entries(fieldValues).forEach(([id, val]) => {
        const input = document.getElementById(id);
        if (input) {
          input.value = val;
          input.classList.add("input-highlight");
          setTimeout(() => input.classList.remove("input-highlight"), 600);
        }
      });
    });
  }

  if (resetFormBtn) {
    resetFormBtn.addEventListener("click", () => {
      if (confirm("Reset all form fields to default values?")) {
        const textInputs = careerForm.querySelectorAll("input[type='text'], input[type='number'], textarea");
        textInputs.forEach(el => el.value = "");
        const selects = careerForm.querySelectorAll("select");
        selects.forEach(sel => sel.selectedIndex = 0);
        document.getElementById("name")?.focus();
      }
    });
  }

  if (careerForm && loadingOverlay) {
    careerForm.addEventListener("submit", (e) => {
      // Basic client-side sanity check
      const cgpaInput = document.getElementById("cgpa");
      if (cgpaInput) {
        const cgpaVal = parseFloat(cgpaInput.value);
        if (isNaN(cgpaVal) || cgpaVal < 0 || cgpaVal > 10) {
          alert("Please enter a valid CGPA between 0.0 and 10.0.");
          cgpaInput.focus();
          e.preventDefault();
          return;
        }
      }

      // Show processing overlay with progressive status messages
      loadingOverlay.style.display = "flex";
      const statusText = document.getElementById("loading-status-text");
      const subText = document.getElementById("loading-sub-text");

      const stages = [
        { main: "Evaluating Skill Sets...", sub: "Mapping technical competencies against industry rubrics" },
        { main: "Calculating Match Scores...", sub: "Applying 50% Skills, 30% Interests, 20% CGPA rule-based weights" },
        { main: "Generating Personalized Roadmap...", sub: "Compiling 5-step curriculum and priority gap analysis" }
      ];

      let stageIdx = 0;
      const interval = setInterval(() => {
        stageIdx++;
        if (stageIdx < stages.length) {
          if (statusText) statusText.textContent = stages[stageIdx].main;
          if (subText) subText.textContent = stages[stageIdx].sub;
        } else {
          clearInterval(interval);
        }
      }, 500);
    });
  }

  // =========================================================================
  // 2. RESULTS PAGE: ANIMATED PROGRESS BARS
  // =========================================================================
  const progressFills = document.querySelectorAll(".progress-bar-fill");
  progressFills.forEach(bar => {
    const targetWidth = bar.getAttribute("data-width") || bar.style.width || "0%";
    if (bar.id !== "plan-overall-progress-bar") {
      bar.style.width = "0%";
      setTimeout(() => {
        bar.style.width = targetWidth;
      }, 150);
    }
  });

  // =========================================================================
  // 3. RESULTS PAGE: LOCALSTORAGE LEARNING PLAN TRACKING
  // =========================================================================
  const studentName = document.body.getAttribute("data-student-name") || "student";
  const primaryCareer = document.body.getAttribute("data-career-name") || "career";
  const storageKey = `g2_plan_progress_${encodeURIComponent(studentName)}_${encodeURIComponent(primaryCareer)}`;

  const statusSelects = document.querySelectorAll(".status-select");
  const overallProgressBar = document.getElementById("plan-overall-progress-bar");
  const overallProgressText = document.getElementById("plan-overall-progress-text");

  // Load saved step statuses from localStorage
  function loadPlanProgress() {
    let savedProgress = {};
    try {
      const raw = localStorage.getItem(storageKey);
      if (raw) savedProgress = JSON.parse(raw);
    } catch (e) {
      console.warn("Could not read learning plan progress from localStorage:", e);
    }

    statusSelects.forEach((select, index) => {
      const stepItem = select.closest(".plan-step-item");
      const savedStatus = savedProgress[index] || "Not Started";
      select.value = savedStatus;
      updateStepVisuals(stepItem, savedStatus);
    });

    updateOverallProgress();
  }

  function savePlanProgress() {
    const progressData = {};
    statusSelects.forEach((select, index) => {
      progressData[index] = select.value;
    });

    try {
      localStorage.setItem(storageKey, JSON.stringify(progressData));
    } catch (e) {
      console.warn("Could not write learning plan progress to localStorage:", e);
    }

    updateOverallProgress();
  }

  function updateStepVisuals(stepItem, status) {
    if (!stepItem) return;
    stepItem.classList.remove("status-completed", "status-in-progress", "status-not-started");
    const printStatusText = stepItem.querySelector(".print-status-text");

    if (status === "Completed") {
      stepItem.classList.add("status-completed");
      if (printStatusText) printStatusText.textContent = "Status: Completed ✓";
    } else if (status === "In Progress") {
      stepItem.classList.add("status-in-progress");
      if (printStatusText) printStatusText.textContent = "Status: In Progress ◐";
    } else {
      stepItem.classList.add("status-not-started");
      if (printStatusText) printStatusText.textContent = "Status: Pending ○";
    }
  }

  function updateOverallProgress() {
    if (!statusSelects.length) return;
    let completedCount = 0;
    statusSelects.forEach(sel => {
      if (sel.value === "Completed") completedCount++;
    });

    const totalSteps = statusSelects.length;
    const pct = Math.round((completedCount / totalSteps) * 100);

    if (overallProgressText) {
      overallProgressText.textContent = `${completedCount} of ${totalSteps} Steps Completed (${pct}%)`;
    }
    if (overallProgressBar) {
      overallProgressBar.style.width = `${pct}%`;
    }
  }

  if (statusSelects.length > 0) {
    loadPlanProgress();
    statusSelects.forEach((select) => {
      select.addEventListener("change", (e) => {
        const stepItem = e.target.closest(".plan-step-item");
        updateStepVisuals(stepItem, e.target.value);
        savePlanProgress();
      });
    });
  }

  // =========================================================================
  // 4. RESULTS PAGE: CAREER DETAILS MODAL INTERACTION
  // =========================================================================
  const modal = document.getElementById("career-modal");
  const modalCloseBtn = document.getElementById("modal-close-btn");
  const modalDismissBtn = document.getElementById("modal-dismiss-btn");
  const viewDetailsBtns = document.querySelectorAll(".view-career-details-btn");
  const payloadEl = document.getElementById("career-data-payload");

  let recommendationsData = [];
  if (payloadEl) {
    try {
      recommendationsData = JSON.parse(payloadEl.textContent || "[]");
    } catch (e) {
      console.warn("Could not parse career recommendations payload:", e);
    }
  }

  function openCareerModal(index) {
    const data = recommendationsData[index];
    if (!data || !modal) return;

    // Set Title & Rank
    document.getElementById("modal-career-title").textContent = data.career;
    document.getElementById("modal-career-rank").textContent = `Rank #${index + 1} • ${data.match_percentage}% Match`;
    document.getElementById("modal-career-overview").textContent = data.description;

    // Why You Match Insights
    const whyContainer = document.getElementById("modal-why-match");
    whyContainer.innerHTML = "";
    const reasons = [
      `Deterministic match score: ${data.match_percentage}% based on your profile.`,
      `Verified skills overlap: ${data.matching_skills.length} matching core competencies.`,
      `Targeted curriculum roadmap: 5 sequential steps available to achieve production mastery.`
    ];
    reasons.forEach(r => {
      const pill = document.createElement("div");
      pill.className = "tag-pill recommended";
      pill.style.fontSize = "0.8rem";
      pill.textContent = r;
      whyContainer.appendChild(pill);
    });

    // Matching Skills
    const matchContainer = document.getElementById("modal-matching-skills");
    matchContainer.innerHTML = "";
    if (data.matching_skills && data.matching_skills.length > 0) {
      data.matching_skills.forEach(s => {
        const pill = document.createElement("div");
        pill.className = "tag-pill matching";
        pill.innerHTML = `✓ ${s}`;
        matchContainer.appendChild(pill);
      });
    } else {
      matchContainer.innerHTML = `<span style="font-size: 0.85rem; color: #64748b;">No direct matching baseline skills.</span>`;
    }

    // Skill Gaps
    const gapContainer = document.getElementById("modal-skill-gaps");
    gapContainer.innerHTML = "";
    if (data.skill_gaps && data.skill_gaps.length > 0) {
      data.skill_gaps.forEach(g => {
        const pill = document.createElement("div");
        pill.className = "tag-pill gap";
        pill.innerHTML = `⚠ ${g.skill} (${g.priority})`;
        gapContainer.appendChild(pill);
      });
    } else {
      gapContainer.innerHTML = `<span style="font-size: 0.85rem; color: #065f46;">No major skill gaps identified.</span>`;
    }

    // Recommended Flow
    const flowBox = document.getElementById("modal-learning-path-flow");
    flowBox.textContent = data.learning_path_flow || "Fundamentals → Core Frameworks → Hands-On Projects → Advanced Mastery";

    modal.style.display = "flex";
    document.body.style.overflow = "hidden"; // Prevent background scrolling
  }

  function closeCareerModal() {
    if (!modal) return;
    modal.style.display = "none";
    document.body.style.overflow = "";
  }

  viewDetailsBtns.forEach(btn => {
    btn.addEventListener("click", () => {
      const idx = parseInt(btn.getAttribute("data-career-index"), 10);
      if (!isNaN(idx)) openCareerModal(idx);
    });
  });

  if (modalCloseBtn) modalCloseBtn.addEventListener("click", closeCareerModal);
  if (modalDismissBtn) modalDismissBtn.addEventListener("click", closeCareerModal);

  // Close modal when clicking on the backdrop
  if (modal) {
    modal.addEventListener("click", (e) => {
      if (e.target === modal) closeCareerModal();
    });
  }

  // Close modal with Escape key
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && modal && modal.style.display === "flex") {
      closeCareerModal();
    }
  });

});
