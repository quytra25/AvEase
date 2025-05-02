import axios from 'axios';

// Setup CSRF token for Django
axios.defaults.withCredentials = true  // required to send cookies
axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = 'X-CSRFToken'

const api = axios.create({
    baseURL: 'http://localhost:8000/api/',
    withCredentials: true,
    headers: {
        'Content-Type': 'application/json',
    },
});

export default {
    // Expose CSRF fetch function
    getCsrfToken() {
        return api.get('csrf/');
    },

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