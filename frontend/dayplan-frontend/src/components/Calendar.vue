<template>
  <div class="calendar">
    <div class="calendar-header">
      <button @click="prevMonth">《</button>
      <span>{{ currentYear }}年 {{ currentMonth + 1 }}月</span>
      <button @click="nextMonth">》</button>
    </div>

    <div class="calendar-weekdays">
      <div v-for="day in weekdays" :key="day" class="weekday">
        {{ day }}
      </div>
    </div>

    <div class="calendar-days">
      <div
        v-for="day in daysInMonth"
        :key="day.date"
        :class="['day', {
          today: isToday(day.date),
          selected: isSelected(day.date),
          hasTask: hasTask(day.date)
        }]"
        @click="selectDate(day.date)"
      >
        <span>{{ day.date.getDate() }}</span>
        <div v-if="hasTask(day.date)" class="task-marker"></div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Calendar',
  props: {
    tasks: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      currentDate: new Date(),
      selectedDate: null,
      weekdays: ['日', '一', '二', '三', '四', '五', '六'],
    }
  },
  computed: {
    currentYear() {
      return this.currentDate.getFullYear();
    },
    currentMonth() {
      return this.currentDate.getMonth();
    },
    daysInMonth() {
      const days = [];
      const firstDayOfMonth = new Date(this.currentYear, this.currentMonth, 1);
      const lastDayOfMonth = new Date(this.currentYear, this.currentMonth + 1, 0);
      const numberOfDays = lastDayOfMonth.getDate();

      for (let i = 1; i <= numberOfDays; i++) {
        days.push({
          date: new Date(this.currentYear, this.currentMonth, i),
        });
      }

      return days;
    }
  },
  methods: {
    prevMonth() {
      this.currentDate = new Date(this.currentYear, this.currentMonth - 1, 1);
    },
    nextMonth() {
      this.currentDate = new Date(this.currentYear, this.currentMonth + 1, 1);
    },
    selectDate(date) {
      this.selectedDate = date;
      this.$emit('date-selected', date);
    },
    isToday(date) {
      const today = new Date();
      return (
        date.getFullYear() === today.getFullYear() &&
        date.getMonth() === today.getMonth() &&
        date.getDate() === today.getDate()
      );
    },
    isSelected(date) {
      return (
        this.selectedDate &&
        date.getFullYear() === this.selectedDate.getFullYear() &&
        date.getMonth() === this.selectedDate.getMonth() &&
        date.getDate() === this.selectedDate.getDate()
      );
    },
    hasTask(date) {
      return this.tasks.some(task => {
        const taskDate = new Date(task.due_date);
        return (
          taskDate.getFullYear() === date.getFullYear() &&
          taskDate.getMonth() === date.getMonth() &&
          taskDate.getDate() === date.getDate()
        );
      });
    }
  }
}
</script>

<style scoped>
.calendar {
  width: 320px;
  border: 1px solid #ddd;
  border-radius: 10px;
  padding: 10px;
  background: #fff;
  margin: auto;
}

.calendar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: bold;
  padding-bottom: 10px;
}

button {
  border: none;
  background: #007bff;
  color: white;
  padding: 5px 10px;
  border-radius: 5px;
  cursor: pointer;
}

button:hover {
  background: #0056b3;
}

.calendar-weekdays,
.calendar-days {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  text-align: center;
}

.weekday {
  font-weight: bold;
  padding: 5px 0;
}

.day {
  padding: 10px;
  cursor: pointer;
  position: relative;
  border-radius: 5px;
  transition: 0.2s;
}

.day:hover {
  background: #f0f0f0;
}

.today {
  background: #ffeb3b;
  font-weight: bold;
}

.selected {
  background: #007bff;
  color: white;
  border-radius: 5px;
}

.hasTask {
  position: relative;
}

.task-marker {
  width: 6px;
  height: 6px;
  background: red;
  border-radius: 50%;
  position: absolute;
  bottom: 4px;
  right: 4px;
}
</style>
