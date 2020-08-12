Spiderを実行すると、最初にstart_urls属性に含まれるURLを指すRequestオブジェクトがScrapyのSchedulerに渡され、Webページの取得を待つキューに追加されます（1）。

キューに追加されたRequestオブジェクトは順にDownloaderに渡されます（2）。DownloaderはRequestオブジェクトに指定されたURLのページを取得し、Responseオブジェクトを作成します。

Downloaderの処理が完了すると、ScrapyEngineがSpiderのコールバック関数を呼び出します。デフォルトのコールバック関数はSpiderのparse()メソッドです。コールバック関数には引数としてResponseオブジェクトが渡されるので、ここからリンクやデータを抽出します（3）。コールバック関数ではyield文で複数のオブジェクトを返せます。リンクを抽出して次のページをクロールしたい場合は、Requestオブジェクトをyieldします。データを抽出したい場合は、Itemオブジェクト（またはdict）をyieldします。1つのメソッドでRequestオブジェクトとItemオブジェクトの両方をyieldしても構いませんし、yieldする順序にも制約はありません。Requestオブジェクトをyieldした場合、再びSchedulerのキューに追加されます（1）。

Itemオブジェクトをyieldした場合、FeedExporterに送られ、ファイルなどに保存されます（4）。

SchedulerのキューにRequestが存在する限りSpiderの実行は継続し、すべてのRequestの処理が完了するとSpiderの実行は終了します。



### nobel_viz
Scrape the Nobel Prize winners information (name, country, year, category, etc...) from wikipedia for data visualization project 

### yahoo_news
Scrape Yahoo News top page, and extract title and body on the each news page
