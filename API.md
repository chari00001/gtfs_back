## GTFS Backend API Dokümantasyonu

Bu doküman, FastAPI tabanlı GTFS servisinin tüm REST uç noktalarını, istek/yanıt yapıları ve kurallarıyla birlikte özetler. Sunucu, varsayılan olarak `API_V1_PREFIX` altında yayınlanır.

- Sürüm: 0.1.0
- Base URL: `/api`
- İçerik tipi: `application/json` (aksi belirtilmedikçe)
- Hata formatı: `{ "detail": string | object }`

### Sağlık

- GET `/api/health`
  - Açıklama: Servis durum kontrolü
  - Yanıt 200: `{ "status": "ok" }`

### GTFS Yönetimi

- POST `/api/gtfs/upload`
  - Açıklama: GTFS ZIP yüklemesini başlatır (arka planda işler)
  - İstek: `multipart/form-data`
    - `file`: ZIP (11 GTFS txt dosyasını içeren)
  - Yanıt 200: `{ message, snapshot_id, status_url }`
  - Hatalar: 400 (ZIP değil), 500

- GET `/api/gtfs/upload/{snapshot_id}/status`
  - Açıklama: Yükleme durumunu döner
  - Yanıt 200: `{ snapshot_id, status, total_files, processed_files, errors[], ... }`
  - Hata 404: Upload not found

- GET `/api/gtfs/snapshots`
  - Açıklama: Mevcut snapshot listesini döner
  - Yanıt 200: `{ snapshots: [ { snapshot_id, created_at } ] }`

- DELETE `/api/gtfs/snapshots/{snapshot_id}`
  - Açıklama: Verilen snapshot'ı tüm tablolardan siler (cascade)
  - Yanıt 200: `{ message, deleted_records }`
  - Hatalar: 404 (snapshot yok), 500

- POST `/api/gtfs/cleanup`
  - Açıklama: Eski snapshot'ları temizler, en son `keep_count` adedi bırakılır
  - Query: `keep_count` (int, varsayılan 5)
  - Yanıt 200: `{ message }`

### Ortak Kurallar

- Birçok uç noktada `snapshot_id` query parametresi vardır.
  - Tür: UUID
  - Opsiyonel (listeleme/okuma için), oluşturma sırasında genelde zorunlu.
- Listeleme uç noktalarında `skip` ve `limit` kullanılır.
  - `skip` >= 0, `limit` 1..1000 (varsayılan 100)
- Bulunamayan kaynaklar için 404 döner.

---

## Agency
Prefix: `/api/agency`

Şemalar:
- AgencyRead: `{ agency_id, agency_name, agency_url, agency_timezone, agency_lang?, agency_phone?, agency_fare_url?, agency_email? }`
- AgencyCreate: `AgencyRead` + zorunlu alan: `agency_id` (body)
- AgencyUpdate: tüm alanlar opsiyonel

- GET `/` — Listele
  - Query: `snapshot_id?`, `skip?`, `limit?`
  - 200: `AgencyRead[]`

- GET `/{agency_id}` — Tekil getir
  - Query: `snapshot_id?`
  - 200: `AgencyRead` | 404

- POST `/` — Oluştur
  - Query: `snapshot_id` (UUID, zorunlu)
  - Body: `AgencyCreate`
  - 200: `AgencyRead`

- PUT `/{agency_id}` — Güncelle
  - Query: `snapshot_id?`
  - Body: `AgencyUpdate`
  - 200: `AgencyRead` | 404

- DELETE `/{agency_id}` — Sil
  - Query: `snapshot_id?`
  - 200: `{ message }` | 404

- GET `/search/by-name` — Ada göre ara
  - Query: `name` (zorunlu), `snapshot_id?`
  - 200: `AgencyRead[]`

- GET `/filter/by-timezone` — Zaman dilimine göre
  - Query: `timezone` (zorunlu), `snapshot_id?`
  - 200: `AgencyRead[]`

- GET `/filter/with-contact` — İletişim bilgisi olanlar
  - Query: `contact_type` in { phone, email }, `snapshot_id?`
  - 200: `AgencyRead[]`

- GET `/snapshots/list`
  - 200: `{ ... }` (servis dönüşüne göre)

## Routes
Prefix: `/api/routes`

Şemalar:
- RoutesRead: `{ route_id, agency_id?, route_short_name?, route_long_name?, route_desc?, route_type, route_url?, route_color?, route_text_color? }`
- RoutesCreate: `RoutesRead` + zorunlu `route_id`
- RoutesUpdate: tüm alanlar opsiyonel

- GET `/` — Listele
  - Query: `snapshot_id?`, `skip?`, `limit?`
  - 200: `RoutesRead[]`

- GET `/{route_id}` — Tekil getir
  - Query: `snapshot_id?`
  - 200: `RoutesRead` | 404

- POST `/` — Oluştur
  - Query: `snapshot_id` (UUID, zorunlu)
  - Body: `RoutesCreate`
  - 200: `RoutesRead`

- PUT `/{route_id}` — Güncelle
  - Query: `snapshot_id?`
  - Body: `RoutesUpdate`
  - 200: `RoutesRead` | 404

- DELETE `/{route_id}` — Sil
  - Query: `snapshot_id?`
  - 200: `{ message }` | 404

- GET `/agency/{agency_id}`
  - Query: `snapshot_id?`
  - 200: `RoutesRead[]`

- GET `/type/{route_type}`
  - Query: `snapshot_id?`
  - 200: `RoutesRead[]`

- GET `/search/advanced`
  - Query: `short_name?`, `long_name?`, `route_type? (0..7)`, `agency_id?`, `snapshot_id?`, `skip?`, `limit?`
  - 200: `RoutesRead[]`

- GET `/stats/types`
  - Query: `snapshot_id?`
  - 200: `{ ... }`

- GET `/filter/with-colors`
  - Query: `snapshot_id?`
  - 200: `RoutesRead[]`

## Stops
Prefix: `/api/stops`

Şemalar:
- StopsRead: `{ stop_id, stop_name, stop_desc?, stop_lat, stop_lon, zone_id?, stop_url? }`
- StopsCreate: `StopsRead` + zorunlu `stop_id`
- StopsUpdate: tüm alanlar opsiyonel

- GET `/` — Listele
  - Query: `snapshot_id?`, `skip?`, `limit?`
  - 200: `StopsRead[]`

- GET `/{stop_id}` — Tekil getir
  - Query: `snapshot_id?`
  - 200: `StopsRead` | 404

- POST `/` — Oluştur
  - Query: `snapshot_id` (UUID, zorunlu)
  - Body: `StopsCreate`
  - 200: `StopsRead`

- PUT `/{stop_id}` — Güncelle
  - Query: `snapshot_id?`
  - Body: `StopsUpdate`
  - 200: `StopsRead` | 404

- DELETE `/{stop_id}` — Sil
  - Query: `snapshot_id?`
  - 200: `{ message }` | 404

- GET `/search/by-name`
  - Query: `name` (zorunlu), `snapshot_id?`
  - 200: `StopsRead[]`

- GET `/search/nearby`
  - Query: `latitude` (-90..90), `longitude` (-180..180), `radius_km` (0..50, varsay. 1.0), `snapshot_id?`, `limit? (1..200, varsay. 50)`
  - 200: `[ { stop: StopsRead, distance_km: number } ]`

- GET `/search/in-bounds`
  - Query: `min_lat`, `max_lat`, `min_lon`, `max_lon`, `snapshot_id?`
  - 200: `StopsRead[]`

- GET `/zone/{zone_id}`
  - Query: `snapshot_id?`
  - 200: `StopsRead[]`

- GET `/stats/bounds`
  - Query: `snapshot_id?`
  - 200: `{ ... }`

## Trips
Prefix: `/api/trips`

Şemalar:
- TripsRead: `{ trip_id, route_id?, service_id?, trip_headsign?, direction_id?, block_id?, shape_id? }`
- TripsCreate: `TripsRead` + zorunlu `trip_id`
- TripsUpdate: tüm alanlar opsiyonel

- GET `/` — Listele
  - Query: `snapshot_id?`, `skip?`, `limit?`
  - 200: `TripsRead[]`

- GET `/{trip_id}` — Tekil getir
  - Query: `snapshot_id?`
  - 200: `TripsRead` | 404

- POST `/` — Oluştur
  - Query: `snapshot_id` (UUID, zorunlu)
  - Body: `TripsCreate`
  - 200: `TripsRead`

- GET `/route/{route_id}`
  - Query: `snapshot_id?`
  - 200: `TripsRead[]`

- GET `/service/{service_id}`
  - Query: `snapshot_id?`
  - 200: `TripsRead[]`

- GET `/stats/by-route`
  - Query: `snapshot_id?`
  - 200: `{ ... }`

## Stop Times
Prefix: `/api/stop-times`

Şemalar:
- StopTimesRead: `{ trip_id, stop_sequence, arrival_time?, departure_time?, stop_id?, stop_headsign?, pickup_type?, drop_off_type?, shape_dist_traveled? }`
- StopTimesCreate: `trip_id`, `stop_sequence` + diğer opsiyoneller
- StopTimesUpdate: alanlar opsiyonel

- GET `/` — Listele
  - Query: `snapshot_id?`, `skip?`, `limit?`
  - 200: `StopTimesRead[]`

- POST `/` — Oluştur
  - Query: `snapshot_id` (UUID, zorunlu)
  - Body: `StopTimesCreate`
  - 200: `StopTimesRead`

- GET `/trip/{trip_id}`
  - Query: `snapshot_id?`
  - 200: `StopTimesRead[]`

- GET `/stop/{stop_id}`
  - Query: `snapshot_id?`
  - 200: `StopTimesRead[]`

- GET `/stop/{stop_id}/schedule`
  - Query: `start_time` (HH:MM:SS, varsay. 00:00:00), `end_time` (varsay. 23:59:59), `snapshot_id?`
  - 200: `StopTimesRead[]`

## Shapes
Prefix: `/api/shapes`

Şemalar:
- ShapesRead: `{ shape_id, shape_pt_sequence, shape_pt_lat, shape_pt_lon, shape_dist_traveled? }`
- ShapesCreate: `shape_id`, `shape_pt_sequence`, `shape_pt_lat`, `shape_pt_lon`, `shape_dist_traveled?`
- ShapesUpdate: alanlar opsiyonel

- GET `/` — Listele
  - Query: `snapshot_id?`, `skip?`, `limit?`
  - 200: `ShapesRead[]`

- POST `/` — Oluştur
  - Query: `snapshot_id` (UUID, zorunlu)
  - Body: `ShapesCreate`
  - 200: `ShapesRead`

- GET `/shape/{shape_id}`
  - Query: `snapshot_id?`
  - 200: `ShapesRead[]` (aynı `shape_id` içindeki tüm noktalar)

- GET `/list/shape-ids`
  - Query: `snapshot_id?`
  - 200: `{ shape_ids: string[] }`

## Calendar
Prefix: `/api/calendar`

Şemalar:
- CalendarRead: `{ service_id, monday?, tuesday?, wednesday?, thursday?, friday?, saturday?, sunday?, start_date?, end_date? }`
- CalendarCreate: `service_id` + diğerleri opsiyonel
- CalendarUpdate: alanlar opsiyonel

- GET `/` — Listele
  - Query: `snapshot_id?`, `skip?`, `limit?`
  - 200: `CalendarRead[]`

- GET `/{service_id}`
  - Query: `snapshot_id?`
  - 200: `CalendarRead` | 404

- POST `/`
  - Query: `snapshot_id` (UUID, zorunlu)
  - Body: `CalendarCreate`
  - 200: `CalendarRead`

- GET `/filter/active`
  - Query: `snapshot_id?`
  - 200: `CalendarRead[]`

- GET `/filter/weekend`
  - Query: `snapshot_id?`
  - 200: `CalendarRead[]`

## Calendar Dates
Prefix: `/api/calendar-dates`

Şemalar:
- CalendarDatesRead: `{ service_id, date, exception_type }`
- CalendarDatesCreate: `service_id`, `date`, `exception_type`
- CalendarDatesUpdate: alanlar opsiyonel: `date`, `exception_type`

- GET `/` — Listele
  - Query: `snapshot_id?`, `skip?`, `limit?`
  - 200: `CalendarDatesRead[]`

- POST `/` — Oluştur
  - Query: `snapshot_id` (UUID, zorunlu)
  - Body: `CalendarDatesCreate`
  - 200: `CalendarDatesRead`

- GET `/service/{service_id}`
  - Query: `snapshot_id?`
  - 200: `CalendarDatesRead[]`

- GET `/filter/exceptions`
  - Query: `snapshot_id?`
  - 200: `CalendarDatesRead[]`

## Fare Attributes
Prefix: `/api/fare-attributes`

Şemalar:
- FareAttributesRead: `{ fare_id, agency_id?, price?, currency_type?, payment_method?, transfers?, transfer_duration? }`
- FareAttributesCreate: `fare_id` + opsiyoneller
- FareAttributesUpdate: alanlar opsiyonel

- GET `/` — Listele
  - Query: `snapshot_id?`, `skip?`, `limit?`
  - 200: `FareAttributesRead[]`

- GET `/{fare_id}` — Tekil getir
  - Query: `snapshot_id?`
  - 200: `FareAttributesRead` | 404

- POST `/` — Oluştur
  - Query: `snapshot_id` (UUID, zorunlu)
  - Body: `FareAttributesCreate`
  - 200: `FareAttributesRead`

- GET `/agency/{agency_id}`
  - Query: `snapshot_id?`
  - 200: `FareAttributesRead[]`

- GET `/currency/{currency_type}`
  - Query: `snapshot_id?`
  - 200: `FareAttributesRead[]`

## Fare Rules
Prefix: `/api/fare-rules`

Şemalar:
- FareRulesRead: `{ fare_id, route_id, origin_id?, destination_id?, contains_id? }`
- FareRulesCreate: `fare_id`, `route_id` + opsiyoneller
- FareRulesUpdate: alanlar opsiyonel

- GET `/` — Listele
  - Query: `snapshot_id?`, `skip?`, `limit?`
  - 200: `FareRulesRead[]`

- POST `/` — Oluştur
  - Query: `snapshot_id` (UUID, zorunlu)
  - Body: `FareRulesCreate`
  - 200: `FareRulesRead`

- GET `/route/{route_id}`
  - Query: `snapshot_id?`
  - 200: `FareRulesRead[]`

- GET `/fare/{fare_id}`
  - Query: `snapshot_id?`
  - 200: `FareRulesRead[]`

## Feed Info
Prefix: `/api/feed-info`

Şemalar:
- FeedInfoRead: `{ id, feed_publisher_name?, feed_publisher_url?, feed_lang?, feed_start_date?, feed_end_date?, feed_version?, feed_contact_email?, feed_contact_url? }`
- FeedInfoCreate: `id` (varsayılan "default") + opsiyoneller
- FeedInfoUpdate: alanlar opsiyonel

- GET `/` — Listele
  - Query: `snapshot_id?`, `skip?`, `limit?`
  - 200: `FeedInfoRead[]`

- POST `/` — Oluştur
  - Query: `snapshot_id` (UUID, zorunlu)
  - Body: `FeedInfoCreate`
  - 200: `FeedInfoRead`

- GET `/latest`
  - Query: `snapshot_id?`
  - 200: `FeedInfoRead` | 404

- GET `/publisher/{publisher_name}`
  - Query: `snapshot_id?`
  - 200: `FeedInfoRead[]`

---

### Kimlik Doğrulama

Bu sürümde kimlik doğrulama/end-to-end yetkilendirme uygulanmamıştır. Gerekirse ters proxy veya API Gateway düzeyinde eklenebilir.

### Hata Kodları

- 400: Geçersiz istek (validation, içerik türü vs.)
- 404: Kaynak bulunamadı
- 500: Sunucu hatası

### Notlar

- Tüm tarih alanları ISO-8601 olarak döner.
- Zaman alanları HH:MM:SS biçimindedir.
- Para değerleri ondalık (`string` olarak JSON'da) dönebilir.


