function showHabits() {
    document.getElementById('createBtn').onclick = async () => {
        const habit = {
            title: title.value,
            description: desc.value,
            frequency: freq.value
        };
        await createHabit(habit);
        showHabits();
    };

    renderHabits();
}

async function createHabit(habit) {
    const token = localStorage.getItem("token");
    const res = await fetch("/habits/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify(habit)
    });

    if (!res.ok) {
        const errText = await res.text();
        console.error("Ошибка создания привычки:", errText);
        alert("Не удалось создать привычку");
    }
}


async function renderHabits() {
    const habits = await fetchHabits();
    const list = document.getElementById('habitsList');
    list.innerHTML = '';
    habits.forEach(habit => {
        const isCheckedToday = habit.checked_today;
        const div = document.createElement('div');

        div.innerHTML = `
            <b>${habit.title}</b> — ${habit.description || ''} 
            [${habit.frequency}]
            <button data-id="${habit.id}" class="checkinBtn ${isCheckedToday ? 'checked' : ''}">✔ Сегодня</button>
            <button data-id="${habit.id}" class="editBtn">✏️</button>
            <button data-id="${habit.id}" class="deleteBtn">🗑️</button>
        `;
        list.appendChild(div);
    });

    document.querySelectorAll('.checkinBtn').forEach(btn => {
        btn.onclick = async () => {
            await checkinHabit(btn.dataset.id);
            btn.classList.add("checked");
            alert('Отмечено!');
        };
    });

    document.querySelectorAll('.deleteBtn').forEach(btn => {
        btn.onclick = async () => {
            if (confirm("Удалить привычку?")) {
                await deleteHabit(btn.dataset.id);
                showHabits();
            }
        };
    });

    document.querySelectorAll('.editBtn').forEach(btn => {
        btn.onclick = async () => {
            const habit = habits.find(h => h.id == btn.dataset.id);
            const newTitle = prompt("Новое название:", habit.title);
            const newDesc = prompt("Новое описание:", habit.description);
            const newFreq = prompt("Новая частота:", habit.frequency);

            if (newTitle && newFreq) {
                await updateHabit(habit.id, {
                    title: newTitle,
                    description: newDesc,
                    frequency: newFreq
                });
                showHabits();
            }
        };
    });
}


function logoutUser() {
    localStorage.removeItem("token");
    console.log("Выход выполнен, токен удалён.");
    window.location.href = "/frontend/login.html";
}

document.getElementById("logoutBtn")?.addEventListener("click", logoutUser);

async function deleteHabit(habitId) {
    const token = localStorage.getItem("token");
    const res = await fetch(`/habits/${habitId}`, {
        method: "DELETE",
        headers: {
            "Authorization": `Bearer ${token}`
        }
    });

    if (!res.ok) {
        const error = await res.text();
        console.error("Ошибка удаления:", error);
        alert("Не удалось удалить привычку.");
    }
}

async function updateHabit(habitId, updatedHabit) {
    const token = localStorage.getItem("token");
    const res = await fetch(`/habits/${habitId}`, {
        method: "PUT",
        headers: {
            "Authorization": `Bearer ${token}`,
            "Content-Type": "application/json"
        },
        body: JSON.stringify(updatedHabit)
    });

    if (!res.ok) {
        const error = await res.text();
        console.error("Ошибка обновления:", error);
        alert("Не удалось обновить привычку.");
    }
}


async function fetchHabits() {
    const token = localStorage.getItem("token");
    const res = await fetch("/habits/", {
        headers: {
            "Authorization": `Bearer ${token}`
        }
    });

    if (!res.ok) {
        console.error("Ошибка загрузки привычек");
        return [];
    }

    return await res.json();
}

async function checkinHabit(habitId) {
    const token = localStorage.getItem("token");
    const res = await fetch(`/habits/${habitId}/checkin`, {
        method: "POST",
        headers: {
            "Authorization": `Bearer ${token}`
        }
    });

    if (!res.ok) {
        const error = await res.text();
        console.error("Ошибка при отметке привычки:", error);
        alert("Не удалось отметить привычку.");
    }
}


showHabits();