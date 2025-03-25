// script.js

document.addEventListener('DOMContentLoaded', function () {
    // Formatter para moeda no padrão brasileiro
    const currencyFormatter = new Intl.NumberFormat('pt-BR', {
        style: 'currency',
        currency: 'BRL'
    });

    // Adicionar novo campo de campus
    document.getElementById('addCampus').addEventListener('click', function () {
        const campusList = document.getElementById('campusList');
        const newCampus = document.createElement('div');
        newCampus.classList.add('row', 'mb-3', 'campus-field');
        newCampus.innerHTML = `
      <div class="col-12 col-md-6 mb-2 mb-md-0">
        <input type="text" class="form-control" placeholder="Nome do Campus" name="campus" required>
      </div>
      <div class="col-12 col-md-4 mb-2 mb-md-0">
        <input type="number" step="0.1" min="0" class="form-control" placeholder="Horas Semanais" name="hours" required>
      </div>
      <div class="col-12 col-md-2">
        <button type="button" class="btn btn-danger w-100 remove-campus">Remover</button>
      </div>
    `;
        campusList.appendChild(newCampus);
    });

    // Remover campo de campus
    document.getElementById('campusList').addEventListener('click', function (event) {
        if (event.target && event.target.classList.contains('remove-campus')) {
            const campusField = event.target.closest('.campus-field');
            campusField.remove();
        }
    });

    // Submissão do formulário
    document.getElementById('salaryForm').addEventListener('submit', async function (e) {
        e.preventDefault();

        const hourlyRate = parseFloat(document.getElementById('hourly_rate').value);
        const campusFields = document.querySelectorAll('.campus-field');
        const campuses = [];
        campusFields.forEach(field => {
            const campusName = field.querySelector('input[name="campus"]').value;
            const hours = parseFloat(field.querySelector('input[name="hours"]').value);
            campuses.push({ campus: campusName, hours: hours });
        });

        const payload = {
            hourly_rate: hourlyRate,
            campuses: campuses
        };

        try {
            const response = await fetch('http://127.0.0.1:8000/calcular-salario', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            const resultData = await response.json();
            let resultHtml = '<h2>Resultado</h2>';
            resultHtml += `<p><strong>Salário Semanal Total:</strong> ${currencyFormatter.format(resultData.overall_weekly_salary)}</p>`;
            resultHtml += `<p><strong>Salário Mensal Total:</strong> ${currencyFormatter.format(resultData.overall_monthly_salary)}</p>`;
            resultHtml += '<h3>Detalhamento por Campus</h3>';
            resultHtml += '<ul class="list-group">';
            resultData.details.forEach(item => {
                resultHtml += `
          <li class="list-group-item">
            <strong>${item.campus}</strong>: 
            ${currencyFormatter.format(item.weekly_salary)} (semana), 
            ${currencyFormatter.format(item.monthly_salary)} (mês)
          </li>
        `;
            });
            resultHtml += '</ul>';
            document.getElementById('result').innerHTML = resultHtml;
        } catch (error) {
            console.error('Erro:', error);
            document.getElementById('result').innerHTML = '<div class="alert alert-danger">Erro ao calcular o salário. Tente novamente.</div>';
        }
    });
});
