(function() {
  var fn = function() {

    (function(root) {
      function now() {
        return new Date();
      }

      var force = false;

      if (typeof root._bokeh_onload_callbacks === "undefined" || force === true) {
        root._bokeh_onload_callbacks = [];
        root._bokeh_is_loading = undefined;
      }







      function run_callbacks() {
        try {
          root._bokeh_onload_callbacks.forEach(function(callback) {
            if (callback != null)
              callback();
          });
        } finally {
          delete root._bokeh_onload_callbacks
        }
        console.debug("Bokeh: all callbacks have finished");
      }

      function load_libs(css_urls, js_urls, callback) {
        if (css_urls == null) css_urls = [];
        if (js_urls == null) js_urls = [];

        root._bokeh_onload_callbacks.push(callback);
        if (root._bokeh_is_loading > 0) {
          console.debug("Bokeh: BokehJS is being loaded, scheduling callback at", now());
          return null;
        }
        if (js_urls == null || js_urls.length === 0) {
          run_callbacks();
          return null;
        }
        console.debug("Bokeh: BokehJS not loaded, scheduling load and callback at", now());
        root._bokeh_is_loading = css_urls.length + js_urls.length;

        function on_load() {
          root._bokeh_is_loading--;
          if (root._bokeh_is_loading === 0) {
            console.debug("Bokeh: all BokehJS libraries/stylesheets loaded");
            run_callbacks()
          }
        }

        function on_error() {
          console.error("failed to load " + url);
        }

        for (var i = 0; i < css_urls.length; i++) {
          var url = css_urls[i];
          const element = document.createElement("link");
          element.onload = on_load;
          element.onerror = on_error;
          element.rel = "stylesheet";
          element.type = "text/css";
          element.href = url;
          console.debug("Bokeh: injecting link tag for BokehJS stylesheet: ", url);
          document.body.appendChild(element);
        }

        for (var i = 0; i < js_urls.length; i++) {
          var url = js_urls[i];
          var element = document.createElement('script');
          element.onload = on_load;
          element.onerror = on_error;
          element.async = false;
          element.src = url;
          console.debug("Bokeh: injecting script tag for BokehJS library: ", url);
          document.head.appendChild(element);
        }
      };var element = document.getElementById("08de9ff6-d48a-46f5-bcc6-cc28651d0a10");
      if (element == null) {
        console.error("Bokeh: ERROR: autoload.js configured with elementid '08de9ff6-d48a-46f5-bcc6-cc28651d0a10' but no matching script tag was found. ")
        return false;
      }

      function inject_raw_css(css) {
        const element = document.createElement("style");
        element.appendChild(document.createTextNode(css));
        document.body.appendChild(element);
      }

      var js_urls = ["https://cdn.pydata.org/bokeh/release/bokeh-1.2.0.min.js", "https://cdn.pydata.org/bokeh/release/bokeh-widgets-1.2.0.min.js", "https://cdn.pydata.org/bokeh/release/bokeh-tables-1.2.0.min.js", "https://cdn.pydata.org/bokeh/release/bokeh-gl-1.2.0.min.js"];
      var css_urls = ["https://cdn.pydata.org/bokeh/release/bokeh-1.2.0.min.css", "https://cdn.pydata.org/bokeh/release/bokeh-widgets-1.2.0.min.css", "https://cdn.pydata.org/bokeh/release/bokeh-tables-1.2.0.min.css"];

      var inline_js = [
        function(Bokeh) {
          Bokeh.set_log_level("info");
        },

        function(Bokeh) {

        },

        function(Bokeh) {
          (function() {
            var fn = function() {
              Bokeh.safely(function() {
                (function(root) {
                  function embed_document(root) {

                  var docs_json = '{"c9c14e25-09e0-45d3-891a-64d38907df4b":{"roots":{"references":[{"attributes":{},"id":"1111","type":"UnionRenderers"},{"attributes":{"source":{"id":"1033","type":"ColumnDataSource"}},"id":"1037","type":"CDSView"},{"attributes":{"formatter":{"id":"1107","type":"BasicTickFormatter"},"ticker":{"id":"1013","type":"BasicTicker"}},"id":"1012","type":"LinearAxis"},{"attributes":{},"id":"1023","type":"WheelZoomTool"},{"attributes":{"active_drag":"auto","active_inspect":"auto","active_multi":null,"active_scroll":"auto","active_tap":"auto","tools":[{"id":"1022","type":"PanTool"},{"id":"1023","type":"WheelZoomTool"},{"id":"1024","type":"BoxZoomTool"},{"id":"1025","type":"ResetTool"},{"id":"1026","type":"SaveTool"}]},"id":"1027","type":"Toolbar"},{"attributes":{},"id":"1010","type":"LinearScale"},{"attributes":{},"id":"1025","type":"ResetTool"},{"attributes":{},"id":"1013","type":"BasicTicker"},{"attributes":{"callback":null,"end":30},"id":"1002","type":"Range1d"},{"attributes":{},"id":"1109","type":"BasicTickFormatter"},{"attributes":{"below":[{"id":"1012","type":"LinearAxis"}],"center":[{"id":"1016","type":"Grid"},{"id":"1021","type":"Grid"}],"left":[{"id":"1017","type":"LinearAxis"}],"plot_height":300,"plot_width":300,"renderers":[{"id":"1036","type":"GlyphRenderer"}],"sizing_mode":"scale_width","title":{"id":"1104","type":"Title"},"toolbar":{"id":"1027","type":"Toolbar"},"x_range":{"id":"1001","type":"Range1d"},"x_scale":{"id":"1008","type":"LinearScale"},"y_range":{"id":"1002","type":"Range1d"},"y_scale":{"id":"1010","type":"LinearScale"}},"id":"1005","subtype":"Figure","type":"Plot"},{"attributes":{"formatter":{"id":"1109","type":"BasicTickFormatter"},"ticker":{"id":"1018","type":"BasicTicker"}},"id":"1017","type":"LinearAxis"},{"attributes":{"overlay":{"id":"1110","type":"BoxAnnotation"}},"id":"1024","type":"BoxZoomTool"},{"attributes":{"dimension":1,"ticker":{"id":"1018","type":"BasicTicker"}},"id":"1021","type":"Grid"},{"attributes":{"bottom_units":"screen","fill_alpha":{"value":0.5},"fill_color":{"value":"lightgrey"},"left_units":"screen","level":"overlay","line_alpha":{"value":1.0},"line_color":{"value":"black"},"line_dash":[4,4],"line_width":{"value":2},"render_mode":"css","right_units":"screen","top_units":"screen"},"id":"1110","type":"BoxAnnotation"},{"attributes":{"data_source":{"id":"1033","type":"ColumnDataSource"},"glyph":{"id":"1034","type":"Scatter"},"hover_glyph":null,"muted_glyph":null,"nonselection_glyph":{"id":"1035","type":"Scatter"},"selection_glyph":null,"view":{"id":"1037","type":"CDSView"}},"id":"1036","type":"GlyphRenderer"},{"attributes":{"text":""},"id":"1104","type":"Title"},{"attributes":{},"id":"1026","type":"SaveTool"},{"attributes":{"callback":null,"end":30},"id":"1001","type":"Range1d"},{"attributes":{"fill_alpha":{"value":0.1},"fill_color":{"value":"#1f77b4"},"line_alpha":{"value":0.1},"line_color":{"value":"#1f77b4"},"size":{"units":"screen","value":12},"x":{"field":"x"},"y":{"field":"y"}},"id":"1035","type":"Scatter"},{"attributes":{"callback":null,"data":{"x":[0,1,2,3,4,5,6,7,8,9,10],"y":[0,8,2,4,6,9,5,6,25,28,4,7]},"selected":{"id":"1112","type":"Selection"},"selection_policy":{"id":"1111","type":"UnionRenderers"}},"id":"1033","type":"ColumnDataSource"},{"attributes":{"ticker":{"id":"1013","type":"BasicTicker"}},"id":"1016","type":"Grid"},{"attributes":{},"id":"1018","type":"BasicTicker"},{"attributes":{},"id":"1022","type":"PanTool"},{"attributes":{},"id":"1008","type":"LinearScale"},{"attributes":{},"id":"1107","type":"BasicTickFormatter"},{"attributes":{},"id":"1112","type":"Selection"},{"attributes":{"fill_alpha":{"value":0.5},"fill_color":{"value":"red"},"line_alpha":{"value":0.5},"line_color":{"value":"red"},"size":{"units":"screen","value":12},"x":{"field":"x"},"y":{"field":"y"}},"id":"1034","type":"Scatter"}],"root_ids":["1005"]},"title":"Bokeh Application","version":"1.2.0"}}';
                  var render_items = [{"docid":"c9c14e25-09e0-45d3-891a-64d38907df4b","roots":{"1005":"08de9ff6-d48a-46f5-bcc6-cc28651d0a10"}}];
                  root.Bokeh.embed.embed_items(docs_json, render_items);

                  }
                  if (root.Bokeh !== undefined) {
                    embed_document(root);
                  } else {
                    var attempts = 0;
                    var timer = setInterval(function(root) {
                      if (root.Bokeh !== undefined) {
                        embed_document(root);
                        clearInterval(timer);
                      }
                      attempts++;
                      if (attempts > 100) {
                        console.log("Bokeh: ERROR: Unable to run BokehJS code because BokehJS library is missing");
                        clearInterval(timer);
                      }
                    }, 10, root)
                  }
                })(window);
              });
            };
            if (document.readyState != "loading") fn();
            else document.addEventListener("DOMContentLoaded", fn);
          })();
        },
        function(Bokeh) {} // ensure no trailing comma for IE
      ];

      function run_inline_js() {

        for (var i = 0; i < inline_js.length; i++) {
          inline_js[i].call(root, root.Bokeh);
        }

      }

      if (root._bokeh_is_loading === 0) {
        console.debug("Bokeh: BokehJS loaded, going straight to plotting");
        run_inline_js();
      } else {
        load_libs(css_urls, js_urls, function() {
          console.debug("Bokeh: BokehJS plotting callback run at", now());
          run_inline_js();
        });
      }
    }(window));
  };
  if (document.readyState != "loading") fn();
  else document.addEventListener("DOMContentLoaded", fn);
})();
