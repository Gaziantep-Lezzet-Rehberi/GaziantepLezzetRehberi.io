from app import db, Recipe, Place, app


def seed():
    with app.app_context():
        db.create_all()

        # helper to add recipe if slug not present
        def add_recipe(data):
            if Recipe.query.filter_by(slug=data['slug']).first():
                return False
            r = Recipe(**data)
            db.session.add(r)
            return True

        # helper to add place if name not present
        def add_place(data):
            if Place.query.filter_by(name=data['name']).first():
                return False
            p = Place(**data)
            db.session.add(p)
            return True

        created = False

        # Core examples (keep existing ones if present)
        created |= add_recipe({
            'name':'Beyran', 'slug':'beyran', 'category':'Çorbalar', 'is_meat':True,
            'cook_time':60, 'difficulty':'Orta', 'servings':4,
            'description':'Gaziantep usulü acılı et suyu çorbası.',
            'ingredients':'Kuzu eti, pirinç, sarımsak, kırmızı biber, tuz, su',
            'steps':'1. Eti haşlayın. 2. Pirinci ekleyin. 3. Baharatları ekleyin.',
            'image_url':'/static/images/beyran.jpg'
        })

        created |= add_recipe({
            'name':'Baklava', 'slug':'baklava', 'category':'Tatlılar', 'is_meat':False,
            'cook_time':90, 'difficulty':'Zor', 'servings':8,
            'description':'İncecik yufkalar ve antep fıstığıyla yapılan tatlı.',
            'ingredients':'Un, su, şeker, tereyağı, Antep fıstığı, şerbet',
            'steps':'1. Yufkaları açın. 2. Fıstık koyun. 3. Pişirin ve şerbet dökün.',
            'image_url':'/static/images/baklava.jpg'
        })

        # Add user-provided list
        more = [
            {'name':'Yuvalama','slug':'yuvalama','category':'Çorbalar','is_meat':True,'cook_time':120,'difficulty':'Zor','servings':6,'description':'Küçük köfteler, nohut ve yoğurtla hazırlanan, özel gün yemeği.','ingredients':"400 g kıyma\n1 su bardağı ince bulgur\n1 adet soğan (rendelenmiş)\n1 çaykaşığı tuz\n1 çaykaşığı karabiber\n1 su bardağı haşlanmış nohut\n4 su bardağı yoğurt\n2 diş sarımsak\n2 yemek kaşığı un","steps":"1. Bulgur, kıyma, rendelenmiş soğan ve baharatları yoğurup küçük köfteler hazırlayın.\n2. Nohutu haşlayın.\n3. Yoğurt, ezilmiş sarımsak ve unu çırpın.\n4. Kaynayan suya köfteleri ve nohutları ekleyip pişirin, ardından yoğurtlu karışımı ekleyin ve karıştırın.", 'image_url':'/static/images/yuvalama.jpg'},
            {'name':'Lebeniye','slug':'lebeniye','category':'Çorbalar','is_meat':False,'cook_time':45,'difficulty':'Kolay','servings':4,'description':'Pirinç ve dövme ile yapılan yoğurtlu çorba.','ingredients':"2 su bardağı yoğurt\n1 su bardağı pirinç\n1/2 su bardağı dövme (haşlanmış)\n1 yemek kaşığı un\n1 çay kaşığı tuz\n1 tatlı kaşığı nane (kuru)\n2 yemek kaşığı tereyağı","steps":"1. Pirinci yıkayıp haşlayın. Eğer dövme kuruysa ayrı haşlayın.\n2. Yoğurt ve unu bir kapta çırpın.\n3. Hafifçe kaynamış pirince yoğurtlu karışımı ekleyin ve karıştırarak pişirin.\n4. Tereyağında naneyi yakıp üzerine gezdirin.", 'image_url':'/static/images/lebeniye.jpg'},
            {'name':'Alinazik','slug':'alinazik','category':'Ana Yemekler','is_meat':True,'cook_time':40,'difficulty':'Orta','servings':4,'description':'Közlenmiş patlıcan püresi üzerine yoğurt ve kıymalı sos konularak servis edilir.','ingredients':"4 adet patlıcan\n2 su bardağı yoğurt\n2 diş sarımsak\n300 g kıyma\n1 adet soğan\n2 yemek kaşığı tereyağı\nTuz, karabiber","steps":"1. Patlıcanları közleyip kabuklarını soyun, püre haline getirin.\n2. Yoğurdu sarımsakla çırpın ve patlıcan püresinin üzerine yayın.\n3. Kıyma ve soğanı kavurup baharatlandırın; yoğurdun üzerine dökerek servis edin.", 'image_url':'/static/images/alinazik.jpg'},
            {'name':'Fıstıklı Kebap','slug':'fistikli-kebap','category':'Ana Yemekler','is_meat':True,'cook_time':50,'difficulty':'Orta','servings':4,'description':'Kıyma içine ince çekilmiş Antep fıstığı konarak hazırlanan özel kebap.','ingredients':"600 g kıyma\n1/2 su bardağı çekilmiş Antep fıstığı\n1 çay kaşığı tuz\n1 çay kaşığı karabiber\n1 yemek kaşığı biber salçası","steps":"1. Kıyma ve çekilmiş fıstığı baharatlarla yoğurun.\n2. Şekil verip ızgarada veya fırında pişirin.\n3. Sıcak servis edin.", 'image_url':'/static/images/fistikli_kebap.jpg'},
            {'name':'Patlıcan Kebabı','slug':'patlican-kebabi','category':'Ana Yemekler','is_meat':True,'cook_time':70,'difficulty':'Orta','servings':4,'description':'Patlıcan ve kıyma katmanlarıyla yapılan fırın yemeği.','ingredients':"4 adet patlıcan\n500 g kıyma\n2 adet domates\n2 adet yeşil biber\nTuz, karabiber, salça","steps":"1. Patlıcanları halka halka doğrayıp kızartın veya közleyin.\n2. Kıyma, doğranmış domates ve biber ile sos hazırlayın.\n3. Kat kat dizip fırında pişirin.", 'image_url':'/static/images/patlican_kebabi.jpg'},
            {'name':'Muhammara','slug':'muhammara','category':'Mezeler','is_meat':False,'cook_time':15,'difficulty':'Kolay','servings':4,'description':'Ceviz, biber salçası ve zeytinyağı ile yapılan ekmek banmalık meze.','ingredients':"2 su bardağı çekilmiş ceviz\n3 yemek kaşığı biber salçası\n2 dilim bayat ekmek\n3 yemek kaşığı zeytinyağı\n1 yemek kaşığı nar ekşisi\nTuz","steps":"1. Ceviz, ekmek ve salçayı robotta çekin.\n2. Zeytinyağı ve nar ekşisini ekleyip kıvam alana kadar çekin.\n3. Servis ederken zeytinyağı gezdirin.", 'image_url':'/static/images/muhammara.jpg'},
            {'name':'İçli Köfte','slug':'icli-kofte','category':'Pilavlar ve Köfteler','is_meat':True,'cook_time':90,'difficulty':'Zor','servings':6,'description':'İnce bulgur dış kabuk ve içindeki özel kıymalı harç ile hazırlanan köfte.','ingredients':"2 su bardağı ince bulgur\n1 su bardağı irmik\n400 g kıyma (iç harç için 250 g)\n1 adet soğan\n1/2 su bardağı ince çekilmiş ceviz\nTuz, karabiber, pul biber","steps":"1. Dış hamuru bulgur ve irmikle yoğurup dinlendirin.\n2. İç harcı kıyma, soğan ve cevizle kavurun.\n3. Hamurdan parçalar koparıp iç harç koyup kapatın.\n4. Kızartın veya haşlayın.", 'image_url':'/static/images/icli_kofte.jpg'},
            {'name':'Ekşili Ufak Köfte','slug':'eksili-ufak-kofte','category':'Pilavlar ve Köfteler','is_meat':True,'cook_time':60,'difficulty':'Orta','servings':4,'description':'Ekşili ve nohutlu sulu köfte yemeği.','ingredients':"250 g kıyma\n1 su bardağı ince bulgur\n1 su bardağı haşlanmış nohut\n2 yemek kaşığı salça\n1 yemek kaşığı sirke\nTuz, karabiber","steps":"1. Küçük köfteler hazırlayın.\n2. Salça, su ve haşlanmış nohutu kaynatın.\n3. Köfteleri ekleyip pişirin.\n4. Sirke ile tadlandırıp servis edin.", 'image_url':'/static/images/eksili_kofte.jpg'},
            {'name':'Öz Çorbası','slug':'oz-corbasi','category':'Pilavlar ve Köfteler','is_meat':True,'cook_time':120,'difficulty':'Zor','servings':6,'description':'Dövme, nohut ve kuşbaşı etle hazırlanan yöresel sulu yemek.','ingredients':"300 g kuşbaşı et\n1 su bardağı dövme\n1 su bardağı nohut\n1 adet soğan\nTuz, karabiber","steps":"1. Eti haşlayın.\n2. Dövme ve nohutu ekleyip uzun süre pişirin.\n3. Tuz ve baharatla tatlandırın.", 'image_url':'/static/images/oz_corbasi.jpg'},
            {'name':'Katmer','slug':'katmer','category':'Tatlılar','is_meat':False,'cook_time':30,'difficulty':'Kolay','servings':2,'description':'İncecik açılan hamurun içine kaymak ve fıstık konularak yapılan kahvaltılık tatlı.','ingredients':"2 yufka\n100 g kaymak\n1/2 su bardağı dövülmüş Antep fıstığı\n2 yemek kaşığı şeker\nTereyağı","steps":"1. Yufkayı açın.\n2. Kaymak ve fıstık karışımını koyup katlayın.\n3. Tereyağında pişirin.", 'image_url':'/static/images/katmer.jpg'},
            {'name':'Havuç Dilimi','slug':'havuc-dilimi','category':'Tatlılar','is_meat':False,'cook_time':45,'difficulty':'Orta','servings':6,'description':'Havuç şeklinde kesilmiş, bol fıstıklı çıtır baklava türü.','ingredients':"250 g tel kadayıf\n150 g Antep fıstığı\n200 g tereyağı\nŞerbet için su ve şeker","steps":"1. Kadayıfı tereyağında kavurun.\n2. İçine fıstık koyup şekil verin.\n3. Pişirip şerbetleyin.", 'image_url':'/static/images/havuc_dilimi.jpg'},
            {'name':'Künefe','slug':'kunefe','category':'Tatlılar','is_meat':False,'cook_time':20,'difficulty':'Kolay','servings':2,'description':'Tel kadayıf, peynir ve şerbet ile yapılan sıcak tatlı.','ingredients':"200 g tel kadayıf\n150 g tuzsuz tel peyniri\n100 g tereyağı\nŞerbet için su ve şeker\nÜzeri için Antep fıstığı","steps":"1. Kadayıfı tereyağında kavurun.\n2. Peynir ekleyip tabaklara bastırın.\n3. Pişirip sıcak şerbet dökün ve fıstık serpin.", 'image_url':'/static/images/kunefe.jpg'},
            {'name':'Menengiç Kahvesi','slug':'menengic-kahvesi','category':'İçecekler','is_meat':False,'cook_time':10,'difficulty':'Kolay','servings':2,'description':'Gaziantep ve Güneydoğu Anadolu’nun karakteristik içeceği; süt veya su ile hazırlanan, kafeinsiz ve fıstığımsı aromalı bir kahve türü.','ingredients':"Kavrulmuş menengiç tohumları veya hazır menengiç tozu\nSüt veya su\nİsteğe bağlı şeker","steps":"1. Menengiç tohumlarını havanda dövün veya hazır tozu kullanın.\n2. Cezveye menengiç ve süt/suyu koyun, kısık ateşte köpürtmeden yavaşça ısıtın.\n3. Fincanlara paylaştırın.", 'image_url':'/static/images/menengic_kahvesi.jpg'},
            {'name':'Meyan Şerbeti','slug':'meyan-serbeti','category':'İçecekler','is_meat':False,'cook_time':60,'difficulty':'Orta','servings':4,'description':'Yaz aylarında ferahlatıcı, hafif acı-tatlı meyan kökü şerbeti.','ingredients':"Kuru meyan kökü\nSu\n(isteğe bağlı) şeker veya bal","steps":"1. Meyan köklerini temizleyip doğrayın.\n2. Soğuk suda bekletip yoğurarak özünü çıkarın.\n3. Süzüp soğuk olarak servis edin; üstten akıtılarak köpürtme yöntemi ile sunulur.", 'image_url':'/static/images/meyan_serbeti.jpg'},
            {'name':'Zahter Çayı','slug':'zahter-cayi','category':'İçecekler','is_meat':False,'cook_time':10,'difficulty':'Kolay','servings':1,'description':'Kurutulmuş zahterten hazırlanan aromatik çay; kahvaltılarda ve kış aylarında tercih edilir.','ingredients':"Kurutulmuş zahter (kekik türü)\nKaynar su\n(isteğe bağlı) bal veya limon","steps":"1. Bir tutam zahter bir bardağa koyun.\n2. Üzerine kaynar su ekleyip 5-10 dakika demleyin.\n3. Bal veya limon ile servis edebilirsiniz.", 'image_url':'/static/images/zahter_cayi.jpg'},
            {'name':'Nar Ekşisi Şerbeti','slug':'nar-eksisi-serbeti','category':'İçecekler','is_meat':False,'cook_time':5,'difficulty':'Kolay','servings':2,'description':'Doğal nar ekşisinin su ile açılarak servis edildiği ferahlatıcı bir içecek.','ingredients':"Kaliteli nar ekşisi\nSoğuk su\nİsteğe bağlı şeker veya bal\nBuz","steps":"1. Bir miktar nar ekşisini soğuk su ile karıştırın.\n2. Tadını dengeleyin; isteğe bağlı şeker veya bal ekleyin.\n3. Buz ile soğuk servis edin.", 'image_url':'/static/images/nar_eksisi_serbeti.jpg'},
            {'name':'Yöresel Ayran','slug':'yoresel-ayran','category':'İçecekler','is_meat':False,'cook_time':5,'difficulty':'Kolay','servings':4,'description':'Gaziantep usulü bol köpüklü ayran; kebap yanında tercih edilir.','ingredients':"Yoğurt\nSoğuk su\nTuz","steps":"1. Yoğurt ve suyu karıştırıp tuz ekleyin.\n2. Mikser veya çırpıcı ile kuvvetli çırpıp köpürtün.\n3. Servisten önce hafifçe havalandırın ve köpüklü olarak sunun.", 'image_url':'/static/images/yoresel-ayran.jpg'},
            {'name':'Küşleme','slug':'kusleme','category':'Ana Yemekler','is_meat':True,'cook_time':15,'difficulty':'Kolay','servings':2,'description':'Kuzunun sırt kısmından çıkan, en yumuşak ve değerli et. Genellikle az baharatla, yüksek ateşte kısa sürede pişirilir.','ingredients':"Küşleme (kuzu sırtı), tuz, karabiber, isteğe bağlı zeytinyağı veya tereyağı","steps":"1. Etin sinir ve zarlarını temizleyin.\n2. Tuz ve karabiberle hafifçe marine edin.\n3. Çok yüksek ateşte kısa sürede mühürleyip servis edin.", 'image_url':'/static/images/kusleme.jpg'},
            {'name':'Simit Kebabı','slug':'simit-kebabi','category':'Kebaplar','is_meat':True,'cook_time':30,'difficulty':'Orta','servings':4,'description':'Kıyma harcına köftelik ince bulgur (simit) katılarak yoğrulur; daha hacimli ve farklı dokulu bir kebap elde edilir.','ingredients':"500 g kıyma\n1 su bardağı ince bulgur (simit)\n1 adet soğan (rendelenmiş)\nTuz, karabiber, pul biber\nİsteğe bağlı baharatlar","steps":"1. İnce bulguru ıslatıp şişmesini bekleyin.\n2. Kıyma, rendelenmiş soğan ve baharatlarla birlikte bulguru yoğurun.\n3. Şekil verip ızgarada veya tavada pişirin.", 'image_url':'/static/images/simit_kebabi.jpg'},
        ]

        for item in more:
            created |= add_recipe(item)

        created |= add_place({'name':'İsmet Paşa Kebapçısı','address':'Gaziantep Merkez','category':'Kebaplar','lat':37.0662,'lng':37.3833,'description':'Uzun yıllardır hizmet veren meşhur kebapçı.','rating':4.6,'image_url':''})
        created |= add_place({'name':'Baklavacı Güllüoğlu','address':'Gaziantep Baklava Mah.','category':'Tatlıcılar','lat':37.066,'lng':37.383,'description':'Dünyaca ünlü baklava ustası.','rating':4.8,'image_url':''})

        if created:
            db.session.commit()
            print('Seed: new items added')
        else:
            print('Seed: nothing new to add')


if __name__ == '__main__':
    seed()
