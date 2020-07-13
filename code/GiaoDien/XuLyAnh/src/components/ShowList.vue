<template>
  <div >
    <span style="" :class="color" className="text">Ranking theo khoảng cách {{titleA}}</span> 
    <button v-on:click="closeShow" class="btn btn-sm btn-primary">{{statusButton}}</button>
    <div class="row" v-show="showVariable">
      <div v-for="(item,key) in dataProps" :key="key" class="col-3 divImg">
        <img :src="require( `${dataProps[key][1]}`)" alt="img" class="image_result" />
        <small class="caption">Khoảng cách {{titleA}}: {{dataProps[key][0]}} </small >
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  /* eslint-disable */
  name: "showlist",
  data() {
    
    return {
      statusButton:"Đóng",
      showVariable:true
    };
  },
  props: {
    dataProps: {
      default: null,
      
    },
    titleA:{
        type:[String],
        default:"KHông biết"
      },
      color:{
        default:null
      }
  },
  watch: {},
  methods: {
    closeShow(){
      if(this.showVariable==true){
        this.showVariable =false;
      this.statusButton="Mở"
      }
      else{
        this.showVariable =true;
      this.statusButton="Đóng"
      }
      
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.caption {
  font-size: 12px;
}
img {
  float: left;
  position: relative;
  /* min-width: 200px; */
  /* max-width: 300px; */
  padding: 10px;
  width: 100%;
}
.divImg {
  display: inline;
}
button{
  float: left;
}
</style>
