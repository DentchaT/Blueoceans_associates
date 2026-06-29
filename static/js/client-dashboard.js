// static/js/calculator.js
document.addEventListener('DOMContentLoaded', function() {
    // === INTEREST CALCULATOR ===
    const form = document.querySelector('.container_3 form');
    const amountInput = document.getElementById('amount');
    const startDateInput = document.getElementById('stat');
    const endDateInput = document.getElementById('end');
    const percentageOutput = document.getElementById('perc');
    const profitOutput = document.getElementById('prof');
    
    const MONTHLY_RATE = 0.05; // 5% per month

    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault(); // Stop page reload
            
            const principal = parseFloat(amountInput.value);
            const startDate = new Date(startDateInput.value);
            const endDate = new Date(endDateInput.value);
            
            // Validation
            if (isNaN(principal) || principal <= 0) {
                alert('Enter a valid amount');
                return;
            }
            if (!startDateInput.value || !endDateInput.value) {
                alert('Select start and end dates');
                return;
            }
            if (endDate <= startDate) {
                alert('End date must be after start date');
                return;
            }

            // Calculate months between dates
            const months = (endDate.getFullYear() - startDate.getFullYear()) * 12 + 
                           (endDate.getMonth() - startDate.getMonth());
            
            // Handle partial months as fraction
            const daysDiff = endDate.getDate() - startDate.getDate();
            const totalMonths = months + daysDiff / 30;
            
            if (totalMonths <= 0) {
                alert('Period must be at least 1 day');
                return;
            }

            // Compound interest: A = P(1 + r)^n
            const finalAmount = principal * Math.pow(1 + MONTHLY_RATE, totalMonths);
            const profit = finalAmount - principal;
            const totalPercentageGain = (profit / principal) * 100;

            // Display results
            percentageOutput.value = `${totalPercentageGain.toFixed(2)}%`;
            profitOutput.value = `$${finalAmount.toFixed(2)}`;
        });
    }

    // === TOGGLE ABOUT EMF ===
    const toggleButton = document.getElementById("about_emf");
    const paragraph = document.getElementById("emf");

    if (toggleButton && paragraph) {
        toggleButton.addEventListener("click", () => {
            if (window.getComputedStyle(paragraph).display === "none") {
                paragraph.style.display = "block";
            } else {
                paragraph.style.display = "none";
            }
        });
    }
});