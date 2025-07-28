import {defineStore} from 'pinia'
import {fetchTasks, createTask, fetchTaskDetail, updateTask, deleteTask, fetchUserTasks} from '../services/taskApi'

export const useTaskStore = defineStore('task', {
    state: () => ({
        tasks: [],
        loading: false,
        error: null,
        selectedTask: null,
    }),

    actions: {
        // Sadece belirli bir projeye ait taskleri getirir
        loadTasks(projectId) {
            this.loading = true
            this.error = null
            return fetchTasks({project: projectId})
                .then(res => {
                    this.tasks = res.data
                })
                .catch(() => {
                    this.error = 'Görevler alınamadı'
                })
                .finally(() => {
                    this.loading = false
                })
        },
        async loadUserTasks() {
            this.loading = true
            this.error = null
            try {
                const res = await fetchUserTasks()
                this.tasks = res.data  // buradaki tasks senin serializer’da genişletilmiş şekilde dönecek!
            } catch {
                this.error = 'Kullanıcı görevleri alınamadı'
            } finally {
                this.loading = false
            }
        },

        // Yalnızca burada projectId'yi ekle
        async createTask(projectId, data) {
            console.log(projectId)
            this.loading = true
            this.error = null
            const payload = {...data, project: projectId}
            return await createTask(payload)  // <-- yukarıdaki fonksiyon
                .then(res => {
                    this.tasks.push(res.data)
                })
                .catch(() => {
                    this.error = 'Görev eklenemedi'
                    throw new Error('Görev eklenemedi')
                })
                .finally(() => {
                    this.loading = false
                })
        },
        // Task detay, güncelle, sil gibi fonksiyonları da kolayca eklersin
        async loadTaskDetail(taskId) {
            this.loading = true
            this.error = null
            try {
                const res = await fetchTaskDetail(taskId)
                this.selectedTask = res.data
                return res.data
            } finally {
                this.loading = false
            }
        },

        async updateTask(taskId, data) {
            this.loading = true
            this.error = null
            try {
                const res = await updateTask(taskId, data)
                // State'teki task'ı güncelle
                this.tasks = this.tasks.map(task =>
                    task.id === taskId ? {...task, ...res.data} : task
                )
                // Eğer detayda gösteriyorsan onu da güncelle
                if (this.selectedTask && this.selectedTask.id === taskId) {
                    this.selectedTask = {...this.selectedTask, ...res.data}
                }
                return res.data
            } catch {
                this.error = 'Görev güncellenemedi'
            } finally {
                this.loading = false
            }
        },

        deleteTask(taskId) {
            this.loading = true
            this.error = null
            return deleteTask(taskId)
                .then(() => {
                    this.tasks = this.tasks.filter(task => task.id !== taskId)
                })
                .catch(() => {
                    this.error = 'Görev silinemedi'
                })
                .finally(() => {
                    this.loading = false
                })
        },
    }
})
