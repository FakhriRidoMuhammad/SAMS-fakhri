import '../scss/style.scss';
import Vue from 'vue'
import VueResource from 'vue-resource'
import jQuery from 'jquery';
import axios from 'axios'

Vue.use(VueResource);
const http = Vue.http;

export default http

!function ($) {

}(jQuery);
var app = new Vue({
    el: '#app',
    data: {
        path: "",
        loading: true,
        show: true,
        dht22data: "",
        ds18b20data: "",
        weight: "",
        microphone: "",
        info: ""
    },
    mounted() {
        this.get_data()
        this.timer = setInterval(this.get_data, 4000)
    },

    methods: {
        post: function () {
            this.show = false;
            this.loading = true;
            this.$http.post("/", {
                path: this.path
            }).then(response => {
                this.loading = false;
                this.show = true;
            }, response => {

            });
        },

        get_data() {
            axios
                .get('/api')
                .then(response => (
                    this.loading = false,
                        this.info = response.data
                ))
        }
    },
    beforeDestroy() {
        clearInterval(this.timer)
    }
});
