<!DOCTYPEHTML>
<html>
<head>
<metacharset="utf8">
<title>Elasticsearchによる全文検索</title>
<style>
    input { fontsize: 120%; }
    h3 { fontweight: normal; marginbottom: 0; }
    em{fontweight: bold; fontstyle: normal; }
    .link{ color: green; }
    .fragment{ fontsize: 90%; }
</style>
</head>
<body>
    <!-- 検索フォーム -->
    <form>
        <input type="text" name="q" value="{{query}}">
        <input type="submit" value="検索する">
    </form>

    <!-- 検索結果 -->
    <% for page in pages: %>
        <div>
            <h3>
                <a href="{{page["_source"]["url"]}}">{{page["_source"]["title"]}}</a>
            </h3>
            <div class="link">
                {{page["_source"]["url"]}}
            </div>
            <div class="fragment">
                {{!page["highlight"]["content"][0]}}
            </div>
        </div>
    <%end%>
</body>
</html>