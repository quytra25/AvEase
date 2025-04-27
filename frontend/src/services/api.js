import axios from 'axios';

const api = axios.create({
    baseURL: '/api/',
    headers: {
        'Content-Type': 'application/json',
    },
});

export default {
    // Events
    listEvents() {
        return api.get('events/');
    },
    createEvent(data) {
        return api.post('events/', data);
    },
    getEvent(id) {
        return api.get(`events/${id}/`);
    },
    updateEvent(id, data) {
        return api.patch(`events/${id}/`, data);
    },

    // Participants
    joinEvent(eventId){
        return api.post('participants/', { event: eventId });
    },

    joinEventAsGuest(eventID, payload) {
        return api.post('participants/guest/', {
            event: eventID,
            email: payload.email
        })
    },

    // Availabilities
    addAvailability(payload){
        return api.post('availabilities/', payload);
    },

};