module default {
    abstract type Auditable {
        required created_at: datetime {
            readonly := true;
            rewrite insert using (datetime_of_statement());
        };
        required updated_at: datetime {
            readonly := true;
            rewrite insert, update using (datetime_of_statement());
        };
    }

    type Source extending Auditable {
        required title: str;
        required url: str;
        required feed_url: str {
            constraint exclusive;
        };
        required health: bool;
    }

    type News extending Auditable {
        required source: Source;
        required internal_id: str;
        required title: str;
        required url: str;
        description: str;
        publication_date: datetime;

        constraint exclusive on ((.source, .internal_id));
    }

    type User extending Auditable {
        required telegram_id: int64 {
            constraint exclusive;
        };
        multi subscriptions: Source;
    }
}
