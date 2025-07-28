import {defineStore} from 'pinia'
import {
    createProject as apiCreateProject, fetchMyProjects,
    fetchMyTeamsWithProjects,
    fetchProjectDetail, updateProject
} from '../services/projectApi.js'
import {fetchProjectsByTeam} from "../services/projectApi.js";

export const useProjectStore = defineStore('project', {
    state: () => ({
        projects: [],
        teamProjects: [],
        teamsWithProjects: [],
        selectedProject: [],
    }),
    actions: {
        async createProject(data) {
            const {data: newProject} = await apiCreateProject(data)
            this.projects.push(newProject)
            return newProject
        },
        async fetchProjectsByTeam(teamId) {
            const {data} = await fetchProjectsByTeam(teamId)
            this.teamProjects = data
            return {data}
        },
        async loadMyTeamsWithProjects() {
            const {data} = await fetchMyTeamsWithProjects()
            this.teamsWithProjects = data
        },
        async loadProjectDetail(projectId) {
            this.loading = true
            this.error = null
            const {data} = await fetchProjectDetail(projectId)
            console.log(data)
            this.selectedProject = data
            console.log(this.selectedProject)
        },

        async updateProject(projectId, data) {
            const {data: updated} = await updateProject(projectId, data)
            // Store’daki listeyi de güncelle (opsiyonel)
            const index = this.projects.findIndex(p => p.id === projectId)
            if (index !== -1) {
                this.projects[index] = {...this.projects[index], ...updated}
            }
            return updated
        },
        async fetchMyProjects() {
            const {data} = await fetchMyProjects(); // api fonksiyonun dönüyor
            this.projects = data;
            return {data}; // <-- Böyle döndür, yoksa undefined gelir!
        }
    }
})


