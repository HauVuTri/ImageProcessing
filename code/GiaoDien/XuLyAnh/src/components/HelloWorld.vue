<template>
  <div>
    <div >
      <form v-on:submit.prevent="matchImage">
        <div class="input-file-container">
          <input
            :class="classInput"
            type="file"
            ref="file"
            @change="onChange"
            class="inputfile"
            id="inputfile"
          />
          <button type="submit" :class="classBtn">Match</button>
          <img v-if="data.file_url!=null" :src="require( `./data/${data.file_url}`)" alt="img" class="image_input" />
        </div>
        <br />
      </form>
      <br />
      <div >
        <ShowList color="text-primary" v-bind:titleA="'Euclidean'" v-bind:dataProps="data.image_match_url"></ShowList>
      </div>
      <br>
    <div >
        <ShowList color ="text-success" v-bind:titleA="'Cosin'" v-bind:dataProps="data.image_match_url_cosine"></ShowList>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import ShowList from "./ShowList";
export default {
  /* eslint-disable */
  name: "xulyanh",
  data() {
    return {
      data: {
        file_url: null,
        image_match_url: [],
        image_match_url_cosine: []
      },

      classInput: "border border-success rounded",
      classBtn: "btn btn-success btn-sm",
      uploadInput: ""
    };
  },
  components: {
    ShowList
  },

  methods: {
    onChange(event) {
      this.uploadInput = this.$refs.file.files[0];
      // this.data.file_url =  URL.createObjectURL(event.target.files[0]);
      // console.log(this.file_url);
      // console.log(event.target.value);
      var str = (event.target.value);
       this.data.file_url = str.slice(12);
       this.data.image_match_url = [];
       this.data.image_match_url_cosine = [];
    },
    async matchImage(event) {
      console.log(1);

      const data = new FormData();
      data.append("file", this.uploadInput);

      // Gọi api tìm kiếm ảnh giống

      var respond = await axios
        .post("http://localhost:5000/search", data, {
          headers: {
            "Content-Type": "multipart/form-data"
          }
        })
        .then(response => {
          this.data.image_match_url = response.data.result_euclidean;
          this.data.image_match_url_cosine = response.data.result_cosine;
          console.log("SUCCESS!!");
        })
        .catch(function() {
          console.log("FAILURE!!");
        });
      // this.data.image_match_url = respond.data.result_euclidean;
      // console.log(this.data.image_match_url)
      // console.log(respond)
    }
  },
  watch: {
    // uploadInput: function() {
    //   if (uploadInput) {
    //     this.classInput = "rounded border border-success";
    //     this.classBtn = "btn btn-success btn-sm";
    //   }
    // }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.image_input{
  max-width:500px ;
}
</style>
