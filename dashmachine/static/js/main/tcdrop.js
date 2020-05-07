let tcdrop_files = {};

function tcdropValidateFilesLength(files, el){
  let max_files = el.find(".tcdrop-form").attr('data-max-files');
  if(max_files === -1){
    tcdropValidateFilesType(files, el);
  } else {
    if (files.length > max_files) {
      el.find('.tcdrop-form').trigger("reset");
      el.find(".tcdrop-error-msg").removeClass('hide');
      el.find(".tcdrop-error-msg-txt").text('Only ' + max_files + ' file(s) are allowed');
    } else {
      tcdropValidateFilesType(files, el);
    }
  }
}

function tcdropValidateFilesType(files, el){
  let allowed_types_str = el.find(".tcdrop-form").attr('data-allowed-types');
  if(allowed_types_str === 'all'){
    tcdropCacheFile(files, el);
    return;
  }
  let allowed_types = allowed_types_str.split(',');
  let x = 0;
  $.each(files, function(){
    let file_ext = this.name.split('.');
    if(allowed_types.includes(file_ext[1])){
      x= x + 1;
    }
  });
  if(x > 0){
    tcdropCacheFile(files, el);
  } else {
    el.find('.tcdrop-form').trigger("reset");
    el.find(".tcdrop-error-msg").removeClass('hide');
    el.find(".tcdrop-error-msg-txt").text('Only ' + allowed_types.toString() + ' files are allowed');
  }
}

function tcdropCacheFile(files, el){
  el.find(".tcdrop-loading-upload").removeClass('hide');
  let url = el.find(".tcdrop-form").attr('data-cache-url');
  let fd = new FormData();
  $.each(files, function(){
    fd.set('file', this);
    $.ajax({
      url: url,
      type: 'POST',
      data: fd,
      cache: false,
      contentType: false,
      processData: false,
      success: function(data){
        tcdrop_files[el.attr("id")].push(data.data.cached);
        el.find(".tcdrop-error-msg").addClass('hide');
        el.find(".tcdrop-files-ul").append(data.data.html);
        el.find('.tcdrop-form').trigger("reset");
        console.log(tcdrop_files);
      }
    }).done(function(){
      tcdropHideDropArea(el);
      el.find(".tcdrop-loading-upload").addClass('hide');
    });
  });
}

function tcdropHideDropArea(el){
  let max_files = el.find(".tcdrop-form").attr('data-max-files');
  if(tcdrop_files[el.attr("id")].length >= max_files){
    el.find(".tcdrop-label").addClass('hide');
  } else {
    el.find(".tcdrop-label").removeClass('hide');
  }
}

function tcdropClearCache(){
  let url = $(".tcdrop-form").attr('data-clear-cache-url');
  $(".tcdrop-form").each(function(e) {
      tcdrop_files[$(this).parent().attr("id")] = [];
  });
  $('.tcdrop-form').trigger("reset");
  $.ajax({
    url: url,
    type: 'GET'
  });
}

function tcdropResetAll(){
  $('.tcdrop-form').trigger("reset");
  $(".tcdrop-error-msg").addClass('hide');
  $(".tcdrop-label").removeClass('hide');
  $(".tcdrop-file-li").addClass('hide');
  tcdropClearCache();
}

function tcdropAddLocalFile(file, url, email_cache="false", el){
  el = $(el);
  el.find(".tcdrop-loading-upload").removeClass('hide');
  $.ajax({
        url: url,
        type: 'GET',
        data: {file: file, email_cache},
        success: function(data){
          tcdrop_files[el.attr("id")].push(data.data.file)
          el.find(".tcdrop-error-msg").addClass('hide');
          el.find(".tcdrop-files-ul").append(data.data.html)
          el.find('.tcdrop-form').trigger("reset");
        }
      }).done(function(){
        tcdropHideDropArea(el);
        el.find(".tcdrop-loading-upload").addClass('hide');
      });
  }
let droppedFiles = false;
function initTCdrop(el){
  el = $(el);
  tcdrop_files[el.attr("id")] = [];
  tcdropClearCache();
  el.find('.tcdrop-form').unbind();
  el.find(".tcdrop-input").unbind();
  el.find(".tcdrop-error-msg-btn").unbind();

  el.find('.tcdrop-form').on('drag dragstart dragend dragover dragenter dragleave drop', function(e) {
    e.preventDefault();
    e.stopPropagation();
  })
  .on('dragover dragenter', function() {
    el.find(".tcdrop-label").addClass('tcdrop-file-hover');
  })
  .on('dragleave dragend drop', function() {
    el.find(".tcdrop-label").removeClass('tcdrop-file-hover');
  })
  .on('drop', function(e) {
    droppedFiles = e.originalEvent.dataTransfer.files;
    el.find(".tcdrop-input").prop("files", e.originalEvent.dataTransfer.files);
    tcdropValidateFilesLength(droppedFiles, el)
  });
  el.find(".tcdrop-input").on('change', function(e){
      let files = this.files;
      tcdropValidateFilesLength(files, el);
  });
  el.find(".tcdrop-error-msg-btn").on('click', function(){
    el.find(".tcdrop-error-msg").addClass('hide');
  });
}
