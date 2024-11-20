module default {
    type Source {
        required title: str;
        required url: str;
        required feed_url: str {
            constraint exclusive;
        };
        required health: bool;
    }
    type News {
        required source: Source;
        required internal_id: str;
        required title: str;
        required url: str;
        description: str;
        publication_date: datetime;
        constraint exclusive on ((.source, .internal_id));
    }
    type User {
        required telegram_id: int64 {
            constraint exclusive;
        };
        multi subscriptions: Source;
    }
}
