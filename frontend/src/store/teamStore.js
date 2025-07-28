import {defineStore} from 'pinia';
import {fetchTeams, fetchTeamDetail, createTeam, addTeamMember, removeTeamMember} from '../services/teamApi.js';

export const useTeamStore = defineStore('team', {
    state: () => ({
        teams: [],
        selectedTeam: null,
    }),
    actions: {
        async logout() {
            this.teams = []
            this.selectedTeam = null
        },
        async loadTeams() {
            const data = await fetchTeams();
            this.teams = data.data
        },
        async loadTeamDetail(teamId) {
            const {data} = await fetchTeamDetail(teamId);
            this.selectedTeam = data;
        },
        async createTeam(teamData) {
            const {data} = await createTeam(teamData);
            this.teams.push(data);
            return data;
        },
        async addMember(teamId, userId) {
            await addTeamMember(teamId, userId);
            await this.loadTeamDetail(teamId); // refresh
        },
        async removeMember(teamId, userId) {
            await removeTeamMember(teamId, userId);
            await this.loadTeamDetail(teamId); // refresh
        },
    },

});
